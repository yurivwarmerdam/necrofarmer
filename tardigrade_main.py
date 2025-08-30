import pygame as pg
from pygame import Vector2
from pygame.sprite import Group
import sys
from scripts.tilemap import Tilemap
from math import floor
from scripts.utils import sheet_to_sprites, load_image
from scripts.camera import Camera

from random import randint

from scripts.custom_sprites import AnimatedSprite, AnimationSequence


pg.init()

display = pg.display.set_mode((80, 60), pg.SCALED, pg.RESIZABLE)

clock = pg.time.Clock()

# tilemap

render_layers = {
    "ground": Group(),
    "paths": Group(),
    "active": Group(),
    "sky": Group(),
    "always_front": Group(),
}

# tile_layer = Group()
# paths_layer = Group()
units = Group()

camera = Camera(
    render_layers,
    Group(),
    display,
    # Vector2(-350, 0),    
    Vector2(0,0),
)
# tilemap = Tilemap("art/tmx/tst_square_map.tmx", {"ground": tile_layer})
tilemap = Tilemap(
    "tilemaps/another_island.tmx",
    {
        "ground": render_layers["ground"],
        "paths": render_layers["paths"],
        "active": render_layers["active"],
    },
)
# anim_layer = Group()

# animated sprite
images_d = sheet_to_sprites(load_image("art/tardigrade.png"), Vector2(80, 80))

seq0 = AnimationSequence(
    images_d[(0, 0)],
    images_d[(1, 0)],
    images_d[(2, 0)],
    images_d[(3, 0)],
)
seq1 = AnimationSequence(
    images_d[(0, 1)],
    images_d[(1, 1)],
    images_d[(2, 1)],
    images_d[(3, 1)],
)
seq2 = AnimationSequence(
    images_d[(0, 2)],
    images_d[(1, 2)],
    images_d[(2, 2)],
    images_d[(3, 2)],
)
seq3 = AnimationSequence(
    images_d[(0, 3)],
    images_d[(1, 3)],
    images_d[(2, 3)],
    images_d[(3, 3)],
)

sprite = AnimatedSprite(
    {"0": seq0, "1": seq1, "2": seq2, "3": seq3},
    Vector2(100, 100),
    units,
    render_layers["active"],
)

clock = pg.time.Clock()

# ---- ticking ----
while True:
    _delta = clock.get_time()
    # --- event loop ---
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pg.mouse.get_pos())
            tile = tilemap.world_to_map(mouse_pos)

            print(f"click: {mouse_pos} : {tile} : [{floor(tile.x)},{floor(tile.y)}]")

    # sprite.set_animation(randint(0, len(sprite.animations) - 1))

    if randint(0, 100) > 99:
        sprite.set_animation(str(randint(0, 3)))
        sprite.flip_h = bool(randint(0, 1))

    # --- update loop ---
    units.update(_delta)

    # --- render loop ---
    # display.fill("darkblue")
    # tile_layer.draw(display)
    # anim_layer.draw(display)

    camera.draw_all()

    pg.display.update()
    clock.tick(60)
