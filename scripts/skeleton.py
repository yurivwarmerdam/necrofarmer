import time
from random import randint, random

from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Sprite

from scripts.entities import PlayerEntity
from scripts.tilemap import Tilemap


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

    def wait(self):
        while True:
            if random() < 0.01:
                return True
            time.sleep(1 / self.sleep_time)

    def pick_player_walk_goal(self):
        return self.player.pos + Vector2(randint(-50, 50), randint(-50, 50))

    def walk_toward_goal(self, goal: Vector2):
        while self.rect.center != goal:
            Vector2(self.rect.center).move_towards(goal, self.walk_speed)
            time.sleep(1 / self.sleep_time)
        return True

    def update(self):
        # TODO: this might work better wiht some subpixel position precision.
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

    # def render(self, surface: Surface):
    #     pg.draw.rect(surface, pg.Color("cyan"), self.rect)
