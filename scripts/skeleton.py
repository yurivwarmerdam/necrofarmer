from random import randint

from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Sprite

from scripts.behaviortree_py.dummy_nodes import Succeeder, Failer, Outputter, Talker
from scripts.entities import ActionStatus
from scripts.tilemap import Tilemap
from scripts.behaviortree_py.behaviortree import (
    SimpleActionNode,
    StatefulActionNode,
    BehaviorTreeFactory,
    NodeStatus,
)
from scripts.player import PlayerEntity
import asyncio
from scripts.async_runner import async_runner
from scripts.global_blackboard import global_blackboard


class WalkTowardsPos(StatefulActionNode):
    def on_start(self) -> NodeStatus:
        # this is the pattern when delegating actions to actual skeleton behavior
        pos = self.get_input("pos")

        self.set_output("action_status", (ActionStatus.RUNNING, "walk_towards", pos))
        super().on_start()

    def on_running(self) -> NodeStatus:
        if self.get_input("action_status") in [ActionStatus.IDLE, ActionStatus.SUCCESS]:
            self.node_status = NodeStatus.SUCCESS
            return self.node_status
        else:
            return NodeStatus.RUNNING


class RandomWait(StatefulActionNode):
    def on_start(self) -> NodeStatus:
        self.task = async_runner().create_task(self.random_sleep)
        super().on_start()

    def on_running(self) -> NodeStatus:
        print(self.task.done())
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
    """this is still TODO"""

    def tick(self) -> NodeStatus:
        goal = global_blackboard().player.pos + Vector2(
            randint(-50, 50), randint(-50, 50)
        )
        self.set_output("goal", goal)
        return NodeStatus.SUCCESS


class Skeleton(Sprite):
    def __init__(
        self,
        game,
        sprite: Surface,
        player: PlayerEntity,
        tilemap: Tilemap,
        pos=Vector2(0, 0),
    ):
        Sprite.__init__(self)
        self.game = game
        self.rect = sprite.get_rect()
        self.rect.center = pos
        self.image = sprite
        self.player = player
        self.tilemap = tilemap

        self.walking = False
        self.walk_goal = Vector2(0, 0)
        self.walk_speed = 110.5
        self.sleep_time = 60

        self.blackboard = {"action_status": ActionStatus.IDLE, "player": self.player}
        nodes = [
            Succeeder,
            Failer,
            Outputter,
            Talker,
            RandomWait,
            WalkTowardsPos,
            StatefulActionNode,
            PickPlayerWalkGoal,
        ]
        factory = BehaviorTreeFactory()
        factory.register_blackboard(self.blackboard)
        factory.register_nodes(nodes)
        self.tree = factory.load_tree_from_xml("simple_bt/trees/skeleton.xml")

    # def pick_player_walk_goal(self):
    #     return self.player.pos + Vector2(randint(-50, 50), randint(-50, 50))

    # def walk_toward_goal(self, goal: Vector2):
    #     while self.rect.center != goal:
    #         Vector2(self.rect.center).move_towards(goal, self.walk_speed)
    #         time.sleep(1 / self.sleep_time)
    #     return True

    def update(self, delta):
        if self.blackboard["action_status"] in [
            ActionStatus.IDLE,
            ActionStatus.SUCCESS,
        ]:
            return
        status, func, params = self.blackboard["action_status"]
        func = getattr(self, func)  # dirty. May need to look in globals, too.
        # func = globals()[func]
        params = eval(params)
        func(delta, params)

    def walk_towards(self, delta, goal: Vector2):
        self.rect.center = Vector2(self.rect.center).move_towards(
            goal, delta * self.walk_speed
        )
        if self.rect.center == goal:
            print("reached goal!")
            self.blackboard["action_status"] = ActionStatus.SUCCESS

    # if not self.walking and random() < 0.01:
    #     self.walk_goal = self.player.pos + Vector2(
    #         randint(-50, 50), randint(-50, 50)
    #     )
    #     self.walk_speed = 0.75 + random() * 0.8
    #     self.walking = True
    #     return
    # elif self.walking:
    #     self.rect.center = Vector2(self.rect.center).move_towards(
    #         self.walk_goal, self.walk_speed
    #     )
    #     if self.rect.center == self.walk_goal:
    #         self.walking = False
    #     return

    def tick(self):
        self.tree.tick()
        pass
