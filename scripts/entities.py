import pygame as pg
from pygame.math import Vector2
from pygame import Surface
from random import randint, random
from scripts.tilemap import Tilemap
from pygame.sprite import Sprite
from pygame.key import ScancodeWrapper
import time

class PlayerEntity:
    def __init__(self, game, e_type, pos, size, sprite, mana=200):
        self.game = game
        self.type = e_type
        self.pos = pos
        self.sprite = sprite
        self.size = size
        self.velocity = Vector2(0, 0)
        self.mana = mana

    def update(self, input_movement: Vector2, keys: ScancodeWrapper):
        frame_movement = input_movement + self.velocity
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surface: Surface):
        surface.blit(self.sprite, self.pos)

    def action(self):
        if self.mana >= 50:
            self.spawn_seed()
            self.mana -= 50

    def spawn_seed(self):
        self.game.seeds.add(
            Seed(self, self.game.assets["seed"], self.game.player.pos),
        )
        pass


class Seed(Sprite):
    def __init__(self, game, sprite, pos=Vector2(0, 0)):
        Sprite.__init__(self)
        self.game = game
        self.rect = sprite.get_rect()
        self.rect.center = pos
        self.image = sprite
        self.pos = pos

    pass


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
        self.sleep_time=60

    def wait(self):
        while True:
            if random() < 0.01:
                return True
            time.sleep(1/self.sleep_time)
        

    def pick_player_walk_goal(self):
        return self.player.pos + Vector2(
                randint(-50, 50), randint(-50, 50)
            )

    def walk_toward_goal(self,goal:Vector2):
        while self.rect.center !=goal:
            Vector2(self.rect.center).move_towards(goal,self.walk_speed)
            time.sleep(1/self.sleep_time)
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
