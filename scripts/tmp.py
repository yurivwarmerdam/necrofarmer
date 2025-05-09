import pygame as pg
import sys
from utils import load_image

screen = pg.display.set_mode((1280, 960))

clock = pg.time.Clock()

sword_guy = load_image("art/sword_guy.png")


# ---- ticking ----
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()
    sword_guy.blit(screen, (50, 50))
    clock.tick(60)
