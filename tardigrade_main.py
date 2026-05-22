import sys

import pygame as pg
import pygame_gui
from pygame import Vector2
from pygame.sprite import Group

from game_scripts import game_tilemap, star
from game_scripts.group_server import get_group_server
from game_scripts.commander import get_commander
from game_scripts.ui.game_ui import MainUI
from game_scripts.tardigrade import Tardigrade
from game_scripts.thopter import Ornithopter
from scripts import image_server
from scripts.camera import initialize_camera


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

display = pg.display.set_mode(
    resolution,
    pg.RESIZABLE,
    # pg.SCALED,
)
# theme is for general settins, buttons for buttons
ui_manager = pygame_gui.UIManager(resolution, theme_path="theme/theme.json")
ui_manager.get_theme().load_theme("theme/buttons_generated.json")
clock = pg.time.Clock()

# -- UI experiments --

ui = MainUI()

# -- group initialization --

group_server = get_group_server()

tilemap = game_tilemap.get_tilemap(
    "tilemaps/another_island.tmx",
)
star.get_star_server(tilemap)

group_server.add_render(tilemap.layers)
group_server.add_render({"draw": Group()})


camera = initialize_camera(
    group_server.render_groups,
    Group(),
    display,
    Vector2(-300, 0),
)

commander = get_commander()
commander.box.add(group_server.render_groups["draw"])

img_server = image_server.get_image_server()


# --- Behavior Tree section ---

BTREE_EVENT = pg.USEREVENT + 1
pg.time.set_timer(BTREE_EVENT, 100)

# -----------------------------


Tardigrade(Vector2(150, 120))
Tardigrade(Vector2(120, 150))
Tardigrade(Vector2(150, 150))

Ornithopter(Vector2(200, 200))


def handle_camera_move():
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


# path_planner = star.get_server(tilemap)


# ---- core loop ----
while True:
    _delta = clock.get_time()

    camera_move = Vector2(0, 0)
    # --- event loop ---
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()
        elif event.type == BTREE_EVENT:
            group_server.behavior_trees.tick()
            break
        elif event.type == pg.VIDEORESIZE:
            camera.set_window_resolution(event.size)
            ui_manager.set_window_resolution(event.size)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                camera.set_zoom(1)
            elif event.key == pg.K_2:
                camera.set_zoom(2)
            elif event.key == pg.K_3:
                camera.set_zoom(3)
            elif event.key == pg.K_4:
                camera.set_zoom(4)

        processed = False
        processed = ui_manager.process_events(event)
        if not processed:
            processed = commander.process_events(event)

    camera_move = handle_camera_move()
    if camera_move != Vector2(0, 0):
        camera.pos += camera_move

    # --- update loop ---
    camera.render_layers["draw"].update()
    group_server.update.update(_delta)
    ui.update(_delta)

    # --- render loop ---
    camera.draw_all()
    ui_manager.update(_delta / 1000)
    ui_manager.draw_ui(display)

    pg.display.update()
    clock.tick(60)
