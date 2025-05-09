import pygame as pg
import sys
from utils import load_image
from entities import CustomSprite
from pygame import Vector2


class TmpPlayer(CustomSprite):
    def __init__(self, pos, image, mana=200):
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos
        self.sprite = image
        self.mana = mana
        self.facing = Vector2(0, -15)


pg.init()

screen = pg.display.set_mode((800, 400))

clock = pg.time.Clock()

sword_guy = load_image("art/sword_guy.png")
debug_rect = pg.rect.Rect(0, 0, 32, 32)
debug_rect.topleft = (0, 0)


TmpPlayer(Vector2(0, 0), load_image("art/dirt.png"))

# basic drawing
pg.draw.rect(screen, "yellow", debug_rect, 1)
pg.draw.circle(screen, "green", (16, 16), 2)
screen.blit(sword_guy, (32, 32))
# /basic drawing

pg.display.update()

# ---- ticking ----
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()
    clock.tick(60)
