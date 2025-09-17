import pygame as pg
from pygame import Vector2
from pygame.sprite import Group, LayeredUpdates
import sys
from scripts.tilemap import Tilemap
from game_scripts.entity_tilemap import EntityTilemap
from scripts.utils import sheet_to_sprites, load_image
from scripts.camera import Camera

from random import randint

from scripts.custom_sprites import AnimatedSprite, AnimationSequence


pg.init()

display = pg.display.set_mode((250, 150), pg.SCALED, pg.RESIZABLE)

clock = pg.time.Clock()

# tilemap

render_layers = {
    "ground": Group(),
    "paths": Group(),
    "active": LayeredUpdates(),
    "sky": Group(),
    "always_front": Group(),
}

units = Group()

camera = Camera(
    render_layers,
    Group(),
    display,
    # Vector2(-125, 0),
    Vector2(0, 0),
)
tilemap = EntityTilemap(
    "tilemaps/another_island.tmx",
    {
        "ground": render_layers["ground"],
        "paths": render_layers["paths"],
        "active": render_layers["active"],
    },
)

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
    anchor="center",
    offset=Vector2(0, 10),
)

clock = pg.time.Clock()


def move_towards(source: Vector2, target: Vector2, by: float):
    delta = target - source
    dist = delta.length()
    if dist <= by or dist == 0:
        return target
    return source + delta.normalize() * by


move_goal = None


def handle_key_input():
    # ----------Alternate way of processing?------------#
    keys_pressed = pg.key.get_pressed()
    camera_move = Vector2(0, 0)
    camera_move.x = (keys_pressed[pg.K_RIGHT] | keys_pressed[pg.K_d]) - (
        keys_pressed[pg.K_LEFT] | keys_pressed[pg.K_a]
    )
    camera_move.y = (keys_pressed[pg.K_DOWN] | keys_pressed[pg.K_s]) - (
        keys_pressed[pg.K_UP] | keys_pressed[pg.K_w]
    )
    return camera_move


# ---- ticking ----
while True:
    _delta = clock.get_time()
    camera_move = Vector2(0, 0)
    # --- event loop ---
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pg.mouse.get_pos())
            tile = tilemap.world_to_map(mouse_pos)
            move_goal = camera.get_global_mouse_pos()

    if move_goal:
        sprite.pos = move_towards(sprite.pos, move_goal, _delta / 10)

    camera_move = handle_key_input()
    if camera_move != Vector2(0, 0):
        camera.pos += camera_move

    # sprite.set_animation(randint(0, len(sprite.animations) - 1))

    if randint(0, 100) > 99:
        sprite.set_animation(str(randint(0, 3)))
        sprite.flip_h = bool(randint(0, 1))

    # --- update loop ---
    units.update(_delta)

    # --- render loop ---
    camera.draw_all()

    pg.display.update()
    clock.tick(60)
