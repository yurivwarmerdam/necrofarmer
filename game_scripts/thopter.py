import pygame as pg
from scripts.custom_sprites import AnimatedSprite
from game_scripts.ui.context_panel import ContextPanel
from game_scripts.selectable import Selectable
from scripts import image_server
from game_scripts import group_server
from pygame.math import Vector2
from random import randint
from scripts.ui_shim import UIButton
from scripts.custom_sprites import integer_scale
from game_scripts.game_tilemap import get_tilemap
from scripts.behaviortree_py.behaviortree import (
    BehaviorTreeFactory,
    SimpleActionNode,
    StatefulActionNode,
    NodeStatus,
    PortsList,
)
from scripts.entities import ActionStatus
from scripts.behaviortree_py.dummy_nodes import Failer, Succeeder, Talker

# TODO:
# - add btree
# - def move (maybe with random target position button)
# - def load
# - def unload
# - def idle (land)
# - def take off


class Ornithopter(AnimatedSprite, Selectable):
    def __init__(self, pos):
        img_server = image_server.get_image_server()
        groups = group_server.get_group_server()
        super().__init__(
            {
                "0": img_server.animations["thopter_0"],
                "1": img_server.animations["thopter_1"],
                "2": img_server.animations["thopter_2"],
                "3": img_server.animations["thopter_3"],
            },
            pos,
            groups.update,
            groups.colliders,
            groups.render_groups["active"],
            groups.behavior_trees,
        )
        self.move_speed = 0.09

        # --- BehaviorTree stuff ---
        self.blackboard = {
            "action_status": ActionStatus.IDLE,
            "self": self,
        }  # minimal required set of blackboard entries.
        nodes = {
            "Succeeder": Succeeder,
            "Failer": Failer,
            "Talker": Talker,
            "PickMoveGoal": PickMoveGoal,
            "MoveTowardsPos": MoveTowardsPos,
            "GetClosestTree": GetClosestTree,
            "TakeWood": TakeWood,
        }  # some sample nodes you'll propbably end up using anyway.
        factory = BehaviorTreeFactory()
        factory.register_blackboard(self.blackboard)
        factory.register_nodes(nodes)
        factory.register_conversion_context(
            {"Vector2": Vector2}
        )  # In case nonstandard datatypes are described in tree.xml, provide mappings here.
        self.tree = factory.load_tree_from_xml(
            "trees/ornithopter.xml"
        )  # where your tree is defined

    def update(self, delta):
        super().update(delta)
        if self.blackboard["action_status"] in [
            ActionStatus.IDLE,
            ActionStatus.SUCCESS,
        ]:
            return
        status, func, params = self.blackboard["action_status"]
        func = getattr(self, func)  # Only class funcs. May need to look in globals.
        func(delta, params)

    def tick(self):
        self.tree.tick()

    @property
    def context_panel(self) -> type[ContextPanel]:
        return OrnithopterPanel

    def move_towards(self, delta, goal: Vector2):
        self.pos = Vector2(self.pos).move_towards(goal, delta * self.move_speed)
        if self.pos == goal:
            self.blackboard["action_status"] = ActionStatus.SUCCESS


# --- Behavior tree section ---


class MoveTowardsPos(StatefulActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList(
            {"pos": Vector2, "get_input": NodeStatus}, {"action_status": NodeStatus}
        )

    def on_start(self) -> NodeStatus:
        # this is the pattern when delegating actions to actual unit behavior
        pos = self.get_input("pos")

        self.set_output("action_status", (ActionStatus.RUNNING, "move_towards", pos))
        return super().on_start()

    def on_running(self) -> NodeStatus:
        if self.get_input("action_status") in [ActionStatus.IDLE, ActionStatus.SUCCESS]:
            self.node_status = NodeStatus.SUCCESS
            return self.node_status
        else:
            return NodeStatus.RUNNING


class PickMoveGoal(SimpleActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList({}, {"goal": Vector2})

    def tick(self) -> NodeStatus:
        goal = self.get_input("self").pos + Vector2(randint(-50, 50), randint(-50, 50))
        self.set_output("goal", goal)
        return NodeStatus.SUCCESS


class MapToWorld(SimpleActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList({"map_pos": Vector2}, {"world_pos": Vector2})

    def tick(self) -> NodeStatus:
        map_pos = self.get_input("map_pos")
        world_pos = get_tilemap().map_to_world(*map_pos)
        self.set_output("world_pos", world_pos)
        return NodeStatus.SUCCESS


class GetClosestTree(SimpleActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList({}, {"wood_pos": Vector2})

    def tick(self) -> NodeStatus:
        pos = self.get_input("self").pos
        map_pos = get_tilemap().world_to_map(pos)
        closest_tree = get_tilemap().get_closest_local_tree_idx(map_pos)
        if closest_tree:
            self.set_output("wood_pos", closest_tree)
            # print(pos, map_pos, closest_tree)
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.FAILURE


class GetClosestBuilding(SimpleActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList({"building_type": str}, {"building_pos": Vector2})

    def tick(self) -> NodeStatus:
        pos = self.get_input("self").pos
        building_type = self.get_input("building_type")
        map_pos = get_tilemap().world_to_map(pos)
        closest_building = get_tilemap().get_closest_local_named_tile_idx(
            map_pos, building_type
        )
        if closest_building:
            self.set_output("building_pos", closest_building)
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.FAILURE


class TakeWood(StatefulActionNode):
    # should become statefulacitonnode with unload speed
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList({}, {"wood_pos": Vector2})

    def tick(self) -> NodeStatus:
        wood_pos = self.get_input("wood_pos")
        result = get_tilemap().take_wood(wood_pos, 1)
        if result is None:
            return NodeStatus.FAILURE
        else:
            return NodeStatus.RUNNING


# --- UI Section ---


class OrnithopterPanel(ContextPanel):
    def __init__(self, *, context_container):
        super().__init__(
            portrait_id="#ornithopter_button",
            context_container=context_container,
        )
        UIButton(
            pg.Rect(0, 0, 54, 46),
            text="",
            object_id="#haul_logs_button",
            scale_func=integer_scale,
            container=context_container,
            command=self.get_closest_tree,
        )

    def get_closest_tree(self):
        pos = self.commander.selected.sprites()[0].pos
        map_pos = get_tilemap().world_to_map(pos)
        closest_tree = get_tilemap().get_closest_local_tree_idx(map_pos)
        # print(pos, map_pos, closest_tree)
