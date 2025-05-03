from random import randint
import pygame as pg

from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Sprite

from scripts.behaviortree_py.dummy_nodes import Succeeder, Failer, Outputter, Talker
from scripts.entities import ActionStatus
from scripts.behaviortree_py.behaviortree import (
    SimpleActionNode,
    StatefulActionNode,
    BehaviorTreeFactory,
    NodeStatus,
)
import asyncio
from scripts.async_runner import async_runner
from scripts.global_blackboard import global_blackboard


class Skeleton(Sprite):
    def __init__(
        self,
        game,
        image: Surface,
        pos=Vector2(0, 0),
    ):
        Sprite.__init__(self)
        self.game = game
        self.rect = image.get_rect()
        self.pos = pos
        self.image = image.copy()

        self.walk_speed = 90
        self.sleep_time = 60

        self.blackboard = {"action_status": ActionStatus.IDLE, "self": self}

        nodes = {
            "Succeeder": Succeeder,
            "Failer": Failer,
            "Outputter": Outputter,
            "Talker": Talker,
            "RandomWait": RandomWait,
            "WalkTowardsPos": WalkTowardsPos,
            "StatefulActionNode": StatefulActionNode,
            "PickPlayerWalkGoal": PickPlayerWalkGoal,
            "IsCloseToPlayer": (IsCloseToPlayer, self),
            "GetFreeSeed": (GetFreeSeed, self),
            "ClaimObject": (ClaimObject, self),
            "WalkTowardsObject": WalkTowardsObject,
            "PickupObject": (PickupObject, self),
        }
        factory = BehaviorTreeFactory()
        factory.register_blackboard(self.blackboard)
        factory.register_nodes(nodes)
        factory.register_conversion_context({"Vector2": Vector2})
        self.tree = factory.load_tree_from_xml("simple_bt/trees/skeleton.xml")
        self.inventory = []

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, value):
        self.rect.center = value

    def update(self, delta):
        if self.blackboard["action_status"] in [
            ActionStatus.IDLE,
            ActionStatus.SUCCESS,
        ]:
            return
        status, func, params = self.blackboard["action_status"]
        func = getattr(self, func)  # Only class funcs. May need to look in globals.
        func(delta, params)

        # -------debug viz ----------:
        # if self == self.game.skeletons.sprites()[1]:
        #     pg.draw.rect(self.image, (255, 0, 0), self.image.get_rect(), width=1)
        # else:
        #     pg.draw.rect(self.image, (0, 255, 0), self.image.get_rect(), width=1)
        # if self.blackboard["action_status"] == ActionStatus.IDLE:
        #     pg.draw.rect(self.image, (255, 0, 0), self.image.get_rect(), width=1)
        # elif self.blackboard["action_status"] == ActionStatus.SUCCESS:
        #     pg.draw.rect(self.image, (0, 255, 0), self.image.get_rect(), width=1)
        # elif self.blackboard["action_status"][0] == ActionStatus.RUNNING:
        #     pg.draw.rect(self.image, (0, 0, 255), self.image.get_rect(), width=1)
        # else:
        #     pg.draw.rect(self.image, (255, 255, 255), self.image.get_rect(), width=1)
        # -------/debug viz ----------

    def walk_towards(self, delta, goal: Vector2):
        self.pos = Vector2(self.pos).move_towards(goal, delta * self.walk_speed)
        if self.pos == goal:
            self.blackboard["action_status"] = ActionStatus.SUCCESS

    def walk_towards_object(self, delta, object: Sprite):
        if hasattr(object, "pos"):
            self.pos = Vector2(self.pos).move_towards(
                object.pos, delta * self.walk_speed
            )
            if self.pos == object.pos:
                self.blackboard["action_status"] = ActionStatus.SUCCESS

    def tick(self):
        self.tree.tick()
        pass


# --------------------- Behaviors ---------------------#


class SimpleSkeletonAction(SimpleActionNode):
    """SimpleActionNode that has a reference to skeleton. Don't forget to register with self."""

    def __init__(self, input_ports, output_ports, skeleton):
        self.skeleton: Skeleton = skeleton
        super().__init__(input_ports=input_ports, output_ports=output_ports)


class IsCloseToPlayer(SimpleSkeletonAction):
    def tick(self) -> NodeStatus:
        dist: Vector2 = global_blackboard().player.pos - self.skeleton.pos
        if dist.magnitude() <= 50:
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.FAILURE


class WalkTowardsPos(StatefulActionNode):
    def on_start(self) -> NodeStatus:
        # this is the pattern when delegating actions to actual skeleton behavior
        pos = self.get_input("pos")

        self.set_output("action_status", (ActionStatus.RUNNING, "walk_towards", pos))
        return super().on_start()

    def on_running(self) -> NodeStatus:
        if self.get_input("action_status") in [ActionStatus.IDLE, ActionStatus.SUCCESS]:
            self.node_status = NodeStatus.SUCCESS
            return self.node_status
        else:
            return NodeStatus.RUNNING


class WalkTowardsObject(StatefulActionNode):
    def on_start(self) -> NodeStatus:
        object = self.get_input("object")
        self.set_output(
            "action_status", (ActionStatus.RUNNING, "walk_towards_object", object)
        )
        return super().on_start()

    def on_running(self) -> NodeStatus:
        if self.get_input("action_status") in [ActionStatus.IDLE, ActionStatus.SUCCESS]:
            self.node_status = NodeStatus.SUCCESS
            return self.node_status
        else:
            return NodeStatus.RUNNING


class RandomWait(StatefulActionNode):
    def on_start(self) -> NodeStatus:
        self.task = async_runner().create_task(self.random_sleep)
        return super().on_start()

    def on_running(self) -> NodeStatus:
        if self.task.done():
            self.node_status = NodeStatus.SUCCESS
        else:
            self.node_status = NodeStatus.RUNNING
        return self.node_status

    async def random_sleep(self):
        wait_time = randint(500, 1500)
        await asyncio.sleep(wait_time / 1000.0)
        return True


class PickPlayerWalkGoal(SimpleActionNode):
    def tick(self) -> NodeStatus:
        goal = global_blackboard().player.pos + Vector2(
            randint(-50, 50), randint(-50, 50)
        )
        self.set_output("goal", goal)
        return NodeStatus.SUCCESS


class GetFreeSeed(SimpleSkeletonAction):
    def tick(self):
        for seed in global_blackboard().seeds:
            if seed.claim(self.skeleton):
                self.set_output("seed", seed)
                self.node_status = NodeStatus.SUCCESS
                return self.node_status
        return NodeStatus.FAILURE


class ClaimObject(SimpleSkeletonAction):
    def tick(self):
        if self.get_input("object").claim(self.skeleton):
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.FAILURE


class PickupObject(SimpleSkeletonAction):
    def tick(self) -> NodeStatus:
        if len(self.skeleton.inventory) == 0:
            object: Sprite = self.get_input("object")
            self.skeleton.inventory.append(object)
            object.kill()
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.FAILURE


class EmptyInventory(SimpleSkeletonAction):
    def tick(self) -> NodeStatus:
        pass
