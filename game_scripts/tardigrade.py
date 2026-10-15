from collections import deque
from random import randint
from time import time

import pygame as pg
from pygame import Vector2
from pygame_gui.core.interfaces.container_interface import IContainerAndContainerLike
from pygame_gui.elements import UILabel

from game_scripts import game_tilemap, star
from game_scripts.commander import get_commander
from game_scripts.selectable import Selectable
from game_scripts.ui.ui_elements import ContextPanel
from scripts.behaviortree_py.behaviortree import NodeStatus
from scripts.behaviortree_py.dummy_nodes import Succeeder
from scripts.camera import get_camera
from scripts.custom_sprites import AnimatedSprite, integer_scale
from scripts.group_server import get_group_server
from scripts.image_server import get_image_server
from scripts.ui_shim import UIButton

from scripts.behaviortree_py.nodes import SimpleActionNode, StatefulActionNode
from scripts.behaviortree_py.factory import BehaviorTreeFactory


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
        self.camera = get_camera()
        self.tilemap = game_tilemap.get_tilemap()
        self.path_planner = star.get_star_server()

        self.path = []

        self.blackboard = {
            "action_status": NodeStatus.IDLE,
            "self": self,
        }
        nodes = {
            "Succeeder": Succeeder,
            "PlanPath": PlanPath,
            "MoveAlongPath": MoveAlongPath,
        }

        factory = BehaviorTreeFactory()
        factory.register_blackboard(self.blackboard)
        factory.register_nodes(nodes)
        factory.register_conversion_context({"Vector2": Vector2})
        self.idle = factory.load_tree_from_xml("trees/tardigrade_idle.xml")
        self.move = factory.load_tree_from_xml("trees/tardigrade_move.xml")
        self.active_tree = self.idle

    def tick(self):
        result = self.active_tree.tick_tree()
        if result != NodeStatus.RUNNING:
            self.active_tree = self.idle

    def update(self, delta):
        # gotta call super because it handles animation frame. May want to separate that out...?
        super().update(delta)

        if randint(0, 100) > 99:
            self.set_animation(str(randint(0, 3)))
            self.flip_h = bool(randint(0, 1))

        if self.path:
            self.pos = self.move_along_path(self.pos, self.path, delta)

    def process_events(self, event: pg.event.Event) -> bool:
        if event.type == pg.MOUSEBUTTONUP and event.button == 3:
            collisions = get_commander().get_mouse_collisions()
            if not collisions:
                self.blackboard["move_goal"] = self.camera.get_global_mouse_pos()

                # move click (if navmesh?)
                # (How to deal with non-navigable clicks like buildings or lakes?)
                # set move goal to whiteboard
                # change active btree to move
                pass
            for c in collisions:
                # if hasattr "build":
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
        start = tuple(self.tilemap.world_to_map(self.pos))
        move_goal = self.camera.get_global_mouse_pos()
        goal = tuple(self.tilemap.world_to_map(move_goal))
        path = self.path_planner.astar(start, goal) or []
        path = deque([self.tilemap.map_to_world(*waypoint) for waypoint in path])
        return path

    def move_towards(self, source: Vector2, target: Vector2, by: float) -> Vector2:
        delta = target - source
        dist = delta.length()
        if dist <= by or dist == 0:
            return target
        return source + delta.normalize() * by

    def move_along_path(
        self, source: Vector2, path: deque[Vector2], by: float
    ) -> Vector2:
        """Note: this consumes path when waypoints are reached."""
        EPS = 1e-9
        move_speed = 0.1
        by *= move_speed
        result = source.copy()
        while by > EPS and path:
            intermediate = self.move_towards(result, path[0], by)
            by -= (intermediate - result).length()
            result = intermediate
            if path[0] == result:
                path.popleft()
        return result

    @property
    def context_panel(self) -> type[ContextPanel]:
        return TardigradePanel


# --- Behavior tree section ---


class PlanPath(SimpleActionNode):
    def tick(self) -> NodeStatus:
        return NodeStatus.SUCCESS


class MoveAlongPath(StatefulActionNode):
    def tick(self) -> NodeStatus:
        return NodeStatus.SUCCESS


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
            object_id="#thopter_button",
            scale_func=integer_scale,
            container=context_container,
            command=self.on_thopter_button_clicked,
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

    def on_thopter_button_clicked(self):
        print(get_commander().selected.sprites()[0])
