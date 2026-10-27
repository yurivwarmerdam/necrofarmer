import weakref
from collections import deque
from random import randint
from time import time

import pygame as pg
from pygame import Vector2
from pygame_gui.core.interfaces.container_interface import IContainerAndContainerLike
from pygame_gui.elements import UILabel

from game_scripts.commander import get_commander
from game_scripts.entity_tilemap import BigTile
from game_scripts.game_tilemap import get_tilemap
from game_scripts.selectable import Selectable
from game_scripts.star import get_star_server
from game_scripts.ui.ui_elements import ContextPanel
from scripts.behaviortree_py.behaviortree import NodeStatus, PortsList
from scripts.behaviortree_py.dummy_nodes import Succeeder
from scripts.behaviortree_py.factory import BehaviorTreeFactory
from scripts.behaviortree_py.nodes import SimpleActionNode, StatefulActionNode
from scripts.camera import get_camera
from scripts.custom_sprites import AnimatedSprite, integer_scale
from scripts.group_server import get_group_server
from scripts.image_server import get_image_server
from scripts.tilemap.tile import Tile
from scripts.ui_shim import UIButton


class Tardigrade(AnimatedSprite, Selectable):
    def __init__(self, pos: Vector2):
        img_server = get_image_server()
        group_server = get_group_server()
        self.collision_mask = 1
        collide_groups = group_server.get_collide_groups_by_mask(self.collision_mask)
        super().__init__(
            {
                "0": img_server.animations["tardigrade_0"],
                "1": img_server.animations["tardigrade_1"],
                "2": img_server.animations["tardigrade_2"],
                "3": img_server.animations["tardigrade_3"],
            },
            pos,
            collide_groups,
            group_server.behavior_trees,
            group_server.update,
            group_server.render_groups["active"],
            anchor="center",
            offset=Vector2(0, 10),
        )

        self.blackboard = {
            "action_status": NodeStatus.IDLE,
            "self": self,
        }
        nodes = {
            "Succeeder": Succeeder,
            "PlanPath": PlanPath,
            "MoveAlongPath": MoveAlongPath,
            "GetTilePos": GetTilePos,
            "Build": Build,
        }

        factory = BehaviorTreeFactory()
        factory.register_blackboard(self.blackboard)
        factory.register_nodes(nodes)
        factory.register_conversion_context({"Vector2": Vector2})
        self.idle_tree = factory.load_tree_from_xml("trees/tardigrade_idle.xml")
        self.move_tree = factory.load_tree_from_xml("trees/tardigrade_move.xml")
        self.build_tree = factory.load_tree_from_xml("trees/tardigrade_build.xml")
        self.active_tree = self.idle_tree

    def tick(self):
        result = self.active_tree.tick_tree()
        if result != NodeStatus.RUNNING:
            self.active_tree = self.idle_tree

    def update(self, delta):
        # gotta call super because it handles animation frame. May want to separate that out...?
        super().update(delta)
        if self.blackboard["action_status"] in [
            NodeStatus.IDLE,
            NodeStatus.SUCCESS,
            NodeStatus.FAILURE,
        ]:
            return

        status, func, params = self.blackboard["action_status"]
        func = getattr(self, func)  # Only class funcs. May need to look in globals.
        func(delta, params)

    def process_events(self, event: pg.event.Event) -> bool:
        if event.type == pg.MOUSEBUTTONUP and event.button == 3:
            collisions = get_commander().get_mouse_collisions()
            if not collisions:
                self.blackboard["click_goal"] = get_camera().get_global_mouse_pos()
                self.move_tree.halt_tree()
                self.active_tree = self.move_tree
                # TODO: How to deal with non-navigable clicks like buildings or lakes?
                pass
            for c in collisions:
                if hasattr(c, "build"):
                    self.blackboard["build_goal"] = weakref.ref(c)
                    self.build_tree.halt_tree()
                    self.active_tree = self.build_tree
                    # set goal to build
                    # change active btree to build
                    pass
        if (
            hasattr(event, "button")
            and event.type == pg.MOUSEBUTTONUP
            and event.button == 3
        ):
            self.path = self.plan_path()
            return True
        else:
            return False

    def plan_path(self):
        start = tuple(get_tilemap().world_to_map(self.pos))
        move_goal = get_camera().get_global_mouse_pos()
        goal = tuple(get_tilemap().world_to_map(move_goal))
        path = get_star_server().astar(start, goal) or []
        path = deque([get_tilemap().map_to_world(*waypoint) for waypoint in path])
        return path

    def move_towards(self, source: Vector2, target: Vector2, by: float) -> Vector2:
        delta = target - source
        dist = delta.length()
        if dist <= by or dist == 0:
            return target
        return source + delta.normalize() * by

    def move_along_path(self, by: float, path: deque[Vector2]) -> None:
        """Note: this consumes path when waypoints are reached."""
        EPS = 1e-9
        move_speed = 0.1
        by *= move_speed
        result = self.pos.copy()
        while by > EPS and path:
            intermediate = self.move_towards(result, path[0], by)
            by -= (intermediate - result).length()
            result = intermediate
            if path[0] == result:
                path.popleft()
        self.pos = result
        if len(path) == 0:
            self.blackboard["action_status"] = NodeStatus.SUCCESS

    @property
    def context_panel(self) -> type[ContextPanel]:
        return TardigradePanel

    def idle(self, _delta):
        if randint(0, 1000) > 999:
            self.set_animation(str(randint(0, 3)))
            self.flip_h = bool(randint(0, 1))

    def build(self, _delta, build_goal: weakref.ref):
        if (not build_goal()) or (not hasattr(build_goal(), "build")):
            self.blackboard["action_status"] = NodeStatus.SUCCESS
            return
        build_goal().build(_delta)  # * build speed


# --- Behavior tree section ---


class GetTilePos(SimpleActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList(
            {"self": Tardigrade, "tile": weakref.ref}, {"pos": Vector2}
        )

    def tick(self) -> NodeStatus:
        trd: Tardigrade = self.get_input("self")
        trd_pos = get_tilemap().world_to_map(trd.pos)
        tile: Tile = self.get_input("tile")()
        self.set_output("pos", tile.pos)
        tile_pos = [get_tilemap().world_to_map(tile.pos)]
        if isinstance(tile, BigTile):
            tile_pos = [t + tile_pos[0] for t in tile.tiles]
        # tile_pos:list[Vector2]
        neighbors = []
        for x in tile_pos:
            neighbors += get_tilemap().get_neighbors(x)
        unique = []
        for i in neighbors:
            if i not in unique and i not in tile_pos:
                unique.append(i)
        walkable = get_star_server().can_walk_nodes(unique)
        sorted_nodes = sorted(walkable, key=lambda v: v.distance_squared_to(trd_pos))
        if not sorted_nodes:
            return NodeStatus.FAILURE
        pos = get_tilemap().map_to_worldv(sorted_nodes[0])
        self.set_output("pos", pos)
        return NodeStatus.SUCCESS


class PlanPath(SimpleActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList(
            {"self": Tardigrade, "goal": Vector2}, {"path": Vector2}
        )

    def tick(self) -> NodeStatus:
        trd = self.get_input("self")
        start = tuple(get_tilemap().world_to_map(trd.pos))
        goal = self.get_input("goal")
        goal = tuple(get_tilemap().world_to_map(goal))
        path = get_star_server().astar(start, goal) or []
        path = deque([get_tilemap().map_to_world(*waypoint) for waypoint in path])
        self.set_output("path", path)
        return NodeStatus.SUCCESS


class MoveAlongPath(StatefulActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList(
            {"path": deque[Vector2], "action_status": NodeStatus},
            {"action_status": NodeStatus},
        )

    def on_start(self) -> NodeStatus:
        # this is the pattern when delegating actions to actual unit behavior
        path = self.get_input("path")
        self.set_output("action_status", (NodeStatus.RUNNING, "move_along_path", path))
        return super().on_start()

    def on_running(self) -> NodeStatus:
        if self.get_input("action_status") in [NodeStatus.IDLE, NodeStatus.SUCCESS]:
            self.node_status = NodeStatus.SUCCESS
            return self.node_status
        else:
            return NodeStatus.RUNNING


class Build(StatefulActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList(
            {"build_goal": Tile, "action_status": NodeStatus},
            {"action_status": NodeStatus},
        )

    def on_start(self) -> NodeStatus:
        build_goal = self.get_input("build_goal")
        self.set_output("action_status", (NodeStatus.RUNNING, "build", build_goal))
        return super().on_start()

    def on_running(self) -> NodeStatus:
        if self.get_input("action_status") in [NodeStatus.IDLE, NodeStatus.SUCCESS]:
            self.node_status = NodeStatus.SUCCESS
            return self.node_status
        else:
            return NodeStatus.RUNNING


# --- UI Section ---


class TardigradePanel(ContextPanel):
    def __init__(self, context_container: IContainerAndContainerLike) -> None:
        super().__init__(
            portrait_id="#tardigrade_button",
            context_container=context_container,
        )
        self.set_context_elems(context_container)

    def set_context_elems(self, context_container: IContainerAndContainerLike):
        UIButton(
            pg.Rect(0, 0, 54, 46),
            text="",
            object_id="#sawmill_button",
            scale_func=integer_scale,
            container=context_container,
            command=self.on_sawmill_button_clicked,
        )
        UILabel(
            pg.Rect(6, 50, 120, 30),
            f"Num selected: {len(get_commander().selected)}",
            container=context_container,
        )
        self.counter = UILabel(
            pg.Rect(70, 20, -1, -1),
            f"Time! {time()}",
            container=context_container,
        )

    def update(self, _delta):
        self.counter.set_text(f"Time! {time()}")

    def on_sawmill_button_clicked(self):
        # print(get_commander().selected.sprites()[0])
        get_commander().cursor.enable_build("sawmill")
