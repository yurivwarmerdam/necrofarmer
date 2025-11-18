import pygame as pg
from pygame import Vector2, Rect, Surface
from pygame.sprite import Group, LayeredUpdates
import sys
from game_scripts.commander import Commander
from scripts.tilemap import Tilemap
from game_scripts import entity_tilemap
from game_scripts.tardigrade import Tardigrade
from scripts.utils import sheet_to_sprites, load_image
from scripts.camera import Camera, initialize_camera
from random import randint
from scripts.custom_sprites import AnimatedSprite, AnimationSequence, NodeSprite
from game_scripts import star
from collections import deque
import pygame_gui
from scripts import image_server
from game_scripts import group_server
from game_scripts.group_server import GroupServer


# Server architecture:
# spin up and have global access to the following:
# - image_server
# - camera
# - star
# - entity_tilemap
# - groups
# in addition, there's also singletons associated with Behavior trees:
# - async_runner
# - global_blackboard


pg.init()

# TODO: Investigate resolutions as per:
# https://www.reddit.com/media?url=https%3A%2F%2Fpreview.redd.it%2Fwsa3qmxrmcm71.png%3Fwidth%3D2468%26format%3Dpng%26auto%3Dwebp%26s%3D6eb4a82822907902e380f2df8c066046a99d7392
# https://www.mwum.com/en/how-to-set-retro-game-resolution-correctly/
# https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpreview.redd.it%2Fvvchz8eyl9371.png%3Fauto%3Dwebp%26s%3D004fd6ef601e3bf843e180e5dd35315893854800&f=1&nofb=1&ipt=54b6ee20bc2fd3b146b6acdf8822f95f0c0521d2fad91546a1749f755325d735

# 1080: 999 v pixels
# 1440: 1359 v pixels

resolution = (636, 333)

display = pg.display.set_mode(resolution, pg.SCALED)  # , pg.RESIZABLE)
clock = pg.time.Clock()

# -- UI experiments --
manager = pygame_gui.UIManager(resolution)
ui_image = load_image("art/tst_ui.png")
image_elem = pygame_gui.elements.UIImage(ui_image.get_rect(), ui_image, manager)

# -- group initialization --

groups = group_server.get_server()

tilemap = entity_tilemap.get_server(
    "tilemaps/another_island.tmx",
)
star.get_server(tilemap)

groups.add_render(tilemap.layers)
units = Group()
render_layers = tilemap.layers.copy()
render_layers["draw"] = Group()

camera = initialize_camera(
    render_layers,
    Group(),
    display,
    Vector2(-125, 0),
    # Vector2(0, 0),
)

commander = Commander()
commander.box.add(render_layers["draw"])

img_server = image_server.get_server()

sprite = AnimatedSprite(
    {
        "0": img_server.animations["tardigrade_0"],
        "1": img_server.animations["tardigrade_1"],
        "2": img_server.animations["tardigrade_2"],
        "3": img_server.animations["tardigrade_3"],
    },
    Vector2(100, 100),
    units,
    render_layers["active"],
    anchor="center",
    offset=Vector2(0, 10),
)

trd = Tardigrade(
    Vector2(150, 150),
    units,
    render_layers["active"],
)

clock = pg.time.Clock()


def move_towards(source: Vector2, target: Vector2, by: float) -> Vector2:
    delta = target - source
    dist = delta.length()
    if dist <= by or dist == 0:
        return target
    return source + delta.normalize() * by


def move_along_path(source: Vector2, path: deque[Vector2], by: float) -> Vector2:
    """Note: this consumes path when waypoints are reached."""
    EPS = 1e-9
    result = source.copy()
    while by > EPS and path:
        intermediate = move_towards(result, path[0], by)
        by -= (intermediate - result).length()
        result = intermediate
        if path[0] == result:
            path.popleft()
    return result


move_goal = None
path = []


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


path_planner = star.get_server(tilemap)

# ---- core loop ----
while True:
    _delta = clock.get_time()

    camera_move = Vector2(0, 0)
    # --- event loop ---
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()
        processed = False
        processed = manager.process_events(event)
        if not processed:
            processed = commander.process_events(event)
        if not processed and event.type == pg.MOUSEBUTTONDOWN:
            start = tuple(tilemap.world_to_map(sprite.pos))
            move_goal = camera.get_global_mouse_pos()
            goal = tuple(tilemap.world_to_map(move_goal))
            path = path_planner.astar(start, goal) or []
            path = deque([tilemap.map_to_world(*pos) for pos in path])

    if path:
        sprite.pos = move_along_path(sprite.pos, path, _delta / 10)

    camera_move = handle_key_input()
    if camera_move != Vector2(0, 0):
        camera.pos += camera_move

    if randint(0, 100) > 99:
        sprite.set_animation(str(randint(0, 3)))
        sprite.flip_h = bool(randint(0, 1))

    # --- update loop ---
    camera.render_layers["draw"].update()
    units.update(_delta)

    # --- render loop ---
    camera.draw_all()
    manager.update(_delta / 1000)
    manager.draw_ui(display)

    pg.display.update()
    clock.tick(60)
