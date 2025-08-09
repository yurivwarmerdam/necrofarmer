from typing import Iterable, override, Optional, List, Any
import sys
import pygame as pg
from pygame import Rect, Surface
from pygame.color import Color
from pygame.math import Vector2
from pygame.sprite import AbstractGroup, Group
from scripts.entities import Seed, BTGroup
from scripts.skeleton import Skeleton
from scripts.utils import load_image
from scripts.tilemap import WorldTilemap
from scripts.ui import ManaBar
from scripts.async_runner import async_runner
from scripts.global_blackboard import global_blackboard
from scripts.player import PlayerEntity


class Camera:
    # relevant source:
    # https://github.com/clear-code-projects/Pygame-Cameras/blob/main/camera.py
    def __init__(
        self,
        layers: dict[str, Group],
        ui: List[Group],
        display: Surface,
        pos=Vector2(0, 0),
        bg_color: Color = Color("blue1"),
    ) -> None:
        self.pos = pos
        self.layers = layers
        self.ui = ui
        self.display = display
        self.bg_color = bg_color

    def get_global_mouse_pos(self):
        return Vector2(pg.mouse.get_pos()) + self.pos

    def draw_all(self):
        self.display.fill(self.bg_color)
        for group in self.layers:
            self.layers[group].draw(self.display)

    def draw_layer(self, layer: Group):
        """Adapted from pygame's cannonical draw logic:
        draw all sprites onto the surface

        Group.draw(surface, special_flags=0): return Rect_list

        Draws all of the member sprites onto the given surface.

        """

        sprites = layer.sprites()
        if hasattr(self.display, "blits"):
            layer.spritedict.update(
                zip(
                    sprites,
                    self.display.blits(
                        (spr.image, spr.rect.move(-self.pos.x, -self.pos.y), None, 0)
                        for spr in sprites  # type: ignore
                    ),
                )
            )
        else:
            for spr in sprites:
                layer.spritedict[spr] = self.display.blit(
                    spr.image, spr.rect.move(-self.pos.x, -self.pos.y), None, 0
                )
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty


class MainClass:
    def __init__(self):
        # initialize
        pg.init()
        # enable screen
        # self.screen = pg.display.set_mode((1280, 960))
        self.display = pg.display.set_mode((640, 480), pg.SCALED, pg.RESIZABLE)

        pg.display.set_caption("test")
        self.clock = pg.time.Clock()

        layers = {
            "ground": Group(),
            "paths": Group(),
            "active": Group(),
            "sky": Group(),
            "always_front": Group(),
        }

        self.movement = Vector2(0, 0)
        self.movement_speed = 3
        self.collision_obstacle = Rect(550, 50, 50, 400)
        self.assets = {
            "fighter": load_image("art/sword_guy.png"),
            "wizard": load_image("art/wand_guy.png"),
            "skeleton": load_image("art/skeleton.png"),
            "dirt": load_image("art/dirt.png"),
            "gravestone": load_image("art/gravestone.png"),
            "tomato": load_image("art/tomato.png"),
            "seed": load_image("art/seed.png"),
        }
        self.player = PlayerEntity(
            self.assets["wizard"], Vector2(50, 50), layers["active"]
        )

        self.seeds = Group()
        Seed(self, self.assets["seed"], Vector2(200, 300),self.seeds,layers["active"])
        

        self.skeletons = BTGroup()
        Skeleton(
            self,
            self.assets["skeleton"],
            Vector2(300, 300),
            self.skeletons,
            layers["active"],
        )
        Skeleton(
            self,
            self.assets["skeleton"],
            Vector2(280, 280),
            self.skeletons,
            layers["active"],
        )
        Skeleton(
            self,
            self.assets["skeleton"],
            Vector2(280, 200),
            self.skeletons,
            layers["active"],
        )
        Skeleton(
            self,
            self.assets["skeleton"],
            Vector2(200, 300),
            self.skeletons,
            layers["active"],
        )
        Skeleton(
            self,
            self.assets["skeleton"],
            Vector2(250, 310),
            self.skeletons,
            layers["active"],
        )
        Skeleton(
            self,
            self.assets["skeleton"],
            Vector2(330, 320),
            self.skeletons,
            layers["active"],
        )
        Skeleton(
            self,
            self.assets["skeleton"],
            Vector2(310, 340),
            self.skeletons,
            layers["active"],
        )
        Skeleton(
            self,
            self.assets["skeleton"],
            Vector2(325, 317),
            self.skeletons,
            layers["active"],
        )

        # self.tilemap: WorldTilemap = WorldTilemap("art/tmx/field.tmx")
        self.tilemap: WorldTilemap = WorldTilemap(
            "/c/dev/pygame/necrofarmer/art/tmx/floating_island.tmx"
        )

        self.ui = Group(ManaBar(self))

        self.camera = Camera(layers, [], self.display, Vector2(-200, 0))

        global_blackboard().player = self.player
        global_blackboard().seeds = self.seeds
        global_blackboard().tilemap = self.tilemap

        self.BTREE_EVENT = pg.USEREVENT + 1
        pg.time.set_timer(self.BTREE_EVENT, 250)

    def main(self):
        while True:
            _delta = self.clock.get_time() / 1000.0

            self.handle_events()
            self.handle_key_input()

            # update entities
            self.update_all(_delta)

            # redraws frame
            self.draw_all()
            self.display.blit(
                pg.transform.scale(self.display, self.display.get_size()), (0, 0)
            )
            pg.display.update()
            async_runner().run_once()
            self.clock.tick(60)

    def handle_events(self):
        # Input stuff and quit boilerplate. Consider moving quit to generic outer loop.
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_F8
            ):
                self.quit()
            if event.type == self.BTREE_EVENT:
                self.skeletons.tick()
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        self.player.action1()
                    case pg.K_z:
                        self.player.action2()

    def handle_key_input(self):
        # ----------Alternate way of processing?------------#

        self.keys_pressed = pg.key.get_pressed()
        self.movement = Vector2(0, 0)
        self.movement.x = self.keys_pressed[pg.K_RIGHT] - self.keys_pressed[pg.K_LEFT]
        self.movement.y = self.keys_pressed[pg.K_DOWN] - self.keys_pressed[pg.K_UP]

    def update_all(self, delta):
        self.player.update(delta, self.movement, self.keys_pressed)
        self.seeds.update()
        self.skeletons.update(delta)
        self.ui.update()

    def draw_all(self):
        # fill bg
        self.display.fill((14, 64, 128))
        # draw bg
        # self.tilemap.get_layer("ground").draw(self.display)
        self.camera.draw_layer(self.tilemap.get_layer("ground"))
        # draw entities
        self.seeds.draw(self.display)
        self.skeletons.draw(self.display)
        self.tilemap.get_layer("plants and graves").draw(self.display)
        self.player.draw(self.display)
        self.ui.draw(self.display)

        # Debug Analytics
        pg.draw.rect(self.display, "lightblue", self.player.rect, 1)
        tile = self.tilemap.world_to_map(self.player.pos)
        tile_pos = self.tilemap.map_to_worldv(tile)
        debug_rect = pg.rect.Rect(0, 0, 24, 16)
        debug_rect.topleft = tile_pos
        pg.draw.rect(self.display, "yellow", debug_rect, 1)
        pg.draw.circle(self.display, "darkblue", self.player.pos, 4, 2)

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    MainClass().main()
