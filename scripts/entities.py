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
    """Define base class for Sprite that can have their ownership claimed.
    Ownership should be periodically reclaimed, since the claim will time out after 1 second."""

    def __init__(self):
        self.claim_time: int = -1000
        self.timeout = 1000
        super().__init__(self)

    @property
    def claim_age(self) -> int:
        return get_ticks() - self.claim_time

    def claim(self, owner) -> bool:
        if not self.owner or self.claim_age >= self.timeout or self.owner == owner:
            self.owner = owner
            self.claim_time = get_ticks()
            return True
        else:
            return False

    def is_claimed(self) -> bool:
        if self.owner and self.claim_age <= self.timeout:
            return True
        else:
            return False


class Seed(Passive):
    def __init__(self, game, sprite, pos=Vector2(0, 0)):
        super().__init__(self)
        self.game = game
        self.rect = sprite.get_rect()
        self.rect.center = pos
        self.image = sprite
        self.pos = pos
