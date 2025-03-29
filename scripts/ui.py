import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.font import Font
from pygame.math import Vector2


class ManaBar(Sprite):
    def __init__(self, game, pos=Vector2(0, 0)):
        Sprite.__init__(self)
        self.game = game

        self.image = Surface((64, 16))
        self.image.fill("darkblue")
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.font = Font(None, 16)
        self.text = self.font.render(f"Mana: {game.player.mana}", True, (255, 255, 255))
        self.image.blit(self.text, (0, 0))

    def update(
        self,
    ):
        self.image.fill("darkblue")
        text = self.font.render(f"Mana: {self.game.player.mana}", True, (255, 255, 255))
        self.image.blit(text, (0, 0))
