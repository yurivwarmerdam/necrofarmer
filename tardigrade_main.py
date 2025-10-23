import pygame as pg
from pygame import Vector2, Rect, Surface
from pygame.sprite import Group, LayeredUpdates
import sys
from scripts.tilemap import Tilemap
from game_scripts.entity_tilemap import EntityTilemap
from scripts.utils import sheet_to_sprites, load_image
from scripts.camera import Camera
from random import randint
from scripts.custom_sprites import AnimatedSprite, AnimationSequence, NodeSprite
from game_scripts.star import WalkPath
from collections import deque
import pygame_gui


class Collider:
    """Allows collision to be added to anything with a pos. Generally useful to add to NodeSprites."""

    def __init__(self, collider: Rect, pos: Vector2 = Vector2(0, 0)):
        self.collider = collider
        self.pos = pos

    @property
    def collider(self):
        return self._collision_rect.move(self.pos)

    @collider.setter
    def collider(self, value: Rect):
        self._collision_rect = value


class Clickable(NodeSprite):
    def __init__(
            self,
            image: Surface,
            pos: Vector2 = Vector2(0, 0),
            anchor="topleft",
            offset: Vector2 = Vector2(0, 0),
            collide_rect: Rect = Rect(0, 0,0,0),
            collide_groups,
            *groups,
    ):
        super().__init__(
            image,
            pos,
            anchor,
            offset,
            *groups)




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

# tilemap

tilemap = EntityTilemap(
    "tilemaps/another_island.tmx",
)

render_layers = tilemap.layers
units = Group()

camera = Camera(
    render_layers,
    Group(),
    display,
    Vector2(-125, 0),
    # Vector2(0, 0),
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


path_planner = WalkPath(tilemap)

# ---- core loop ----
while True:
    _delta = clock.get_time()
    camera_move = Vector2(0, 0)
    # --- event loop ---
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()
        if event.type in (
                pg.MOUSEBUTTONDOWN,
                pg.MOUSEBUTTONUP,
                pg.MOUSEWHEEL,
                pg.KEYDOWN,
                pg.KEYUP,
        ):
            pass
            # print("keys!")

        processed = manager.process_events(event)

        if not processed and event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pg.mouse.get_pos())
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
    units.update(_delta)

    # --- render loop ---
    camera.draw_all()

    manager.update(_delta / 1000)
    manager.draw_ui(display)

    pg.display.update()
    clock.tick(60)
