from random import randint, random

import pygame as pg
from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Sprite

from scripts.behaviortree_py.dummy_nodes import Succeeder, Failer, Outputter, Talker
from scripts.entities import PlayerEntity, ActionStatus
from scripts.tilemap import Tilemap
from scripts.behaviortree_py.behaviortree import (
    SimpleActionNode,
    StatefulActionNode,
    BehaviorTreeFactory,
    NodeStatus,
)
import asyncio
from scripts.async_runner import async_runner


class RandomWait(StatefulActionNode):
    pg.time.Clock()
    pg.time.get_ticks()

    # class Wait(AsyncActionNode):
    # Make sure action_node on bb is empty,
    # Do asyncio start_task stuff, await,
    # and monitor in on_running
    def on_start(self):
        # this is the pattern when delegating actions to actual skeleton behavior
        # self.set_output("action_status", (ActionStatus.RUNNING, "wait"))
        self.task = async_runner().create_task(self.random_sleep)

    def on_running(self):
        if self.task.done():
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.RUNNING

    async def random_sleep(self):
        wait_time = randint(0, 1000)
        print("starting random sleep")
        await asyncio.sleep(wait_time / 1000.0)
        print("ending random sleep")
        return True


class PickPlayerWalkGoal(SimpleActionNode):
    def tick(self) -> NodeStatus:
        self.get_input("player").position
        self.set_output("text", "hello world!")
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
        self.walk_speed = 1.15
        self.sleep_time = 60

        self.blackboard = {"action_status": ActionStatus.IDLE, "player": self.player}
        nodes = [Succeeder, Failer, Outputter, Talker,RandomWait]
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
        if self.blackboard["action_status"] == ActionStatus.IDLE:
            return

        status, func, params = self.blackboard["action_status"]

        func(delta, *params)

        if not self.walking and random() < 0.01:
            self.walk_goal = self.player.pos + Vector2(
                randint(-50, 50), randint(-50, 50)
            )
            self.walk_speed = 0.75 + random() * 0.8
            self.walking = True
            return
        elif self.walking:
            self.rect.center = Vector2(self.rect.center).move_towards(
                self.walk_goal, self.walk_speed
            )
            if self.rect.center == self.walk_goal:
                self.walking = False
            return

    def tick(self):
        self.tree.tick()
        pass
