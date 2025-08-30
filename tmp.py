import pygame as pg
from pygame import Vector2, Surface
from pygame.sprite import Group, Sprite
import sys
from scripts.tilemap import Tilemap
from math import floor
from scripts.utils import sheet_to_sprites, load_image
from random import randint
import pyscroll
import pytmx

pg.init()

display = pg.display.set_mode((800, 400), pg.SCALED, pg.RESIZABLE)
clock = pg.time.Clock()

# tilemap

tmx_data = pytmx.load_pygame(
    "tilemaps/another_island.tmx",
)
map_layer = pyscroll.IsometricBufferedRenderer(
    pyscroll.TiledMapData(tmx_data), display.get_size()
)
group = pyscroll.PyscrollGroup(map_layer)
print(group)

# ---- ticking ----
while True:
    _delta = clock.get_time()
    # --- event loop ---
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            pass

    # --- update loop ---
    group.draw(display)
    pg.display.update()
    clock.tick(60)
