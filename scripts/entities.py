from enum import Enum
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from pygame.time import get_ticks
import pygame as pg


class ActionStatus(Enum):
    IDLE = 0
    RUNNING = 1
    SUCCESS = 2
    FAILURE = 3
    SKIPPED = 4


class BTGroup(Group):
    def tick(self, *args, **kwargs):
        """call the tick method of every member sprite

        Group.tick(*args, **kwargs): return None

        Calls the update method of every member sprite. All arguments that
        were passed to this method are passed to the Sprite update function.

        """
        for sprite in self.sprites():
            sprite.tick(*args, **kwargs)


class Passive(Sprite):
    def claim(self) -> bool:
        if self.is_claimed():
            return False
        else:
            self.claimed_tick = get_ticks()
            return True

    def is_claimed(self) -> bool:
        """return False if node hasn't been claimed in the last 5 ticks."""
        if not self.claimed_tick:
            return False
        else:
            delta = get_ticks() - self.claimed_tick
            return not delta > 5


class Seed(Passive):
    def __init__(self, game, sprite, pos=Vector2(0, 0)):
        super().__init__(self)
        self.game = game
        self.rect = sprite.get_rect()
        self.rect.center = pos
        self.image = sprite
        self.pos = pos
