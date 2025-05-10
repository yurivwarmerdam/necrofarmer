import sys
import pygame as pg
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from scripts.entities import Seed, BTGroup
from scripts.skeleton import Skeleton
from scripts.utils import load_image
from scripts.tilemap import WorldTilemap
from scripts.ui import ManaBar
from scripts.async_runner import async_runner
from scripts.global_blackboard import global_blackboard
from scripts.player import PlayerEntity


class MainClass:
    def __init__(self):
        pass
        # initialize
        pg.init()
        # enable screen
        self.screen = pg.display.set_mode((1280, 960))
        self.display = pg.Surface((640, 480))

        pg.display.set_caption("test")
        self.clock = pg.time.Clock()

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
            self.assets["wizard"],
            Vector2(50, 50),
        )

        self.seeds = Group(
            Seed(self, self.assets["seed"], Vector2(200, 300)),
        )

        self.skeletons = BTGroup(
            Skeleton(self, self.assets["skeleton"], Vector2(300, 300)),
            Skeleton(self, self.assets["skeleton"], Vector2(280, 280)),
            Skeleton(self, self.assets["skeleton"], Vector2(280, 200)),
            Skeleton(self, self.assets["skeleton"], Vector2(200, 300)),
            Skeleton(self, self.assets["skeleton"], Vector2(250, 310)),
            Skeleton(self, self.assets["skeleton"], Vector2(330, 320)),
            Skeleton(self, self.assets["skeleton"], Vector2(310, 340)),
            Skeleton(self, self.assets["skeleton"], Vector2(325, 317)),
        )

        self.ui = Group(ManaBar(self))

        self.tilemap: WorldTilemap = WorldTilemap("art/tmx/field.tmx")

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
            self.screen.blit(
                pg.transform.scale(self.display, self.screen.get_size()), (0, 0)
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
        self.tilemap.get_layer("ground").draw(self.display)
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
        debug_rect = pg.rect.Rect(0, 0, 16, 16)
        debug_rect.topleft = tile_pos
        pg.draw.rect(self.display, "yellow", debug_rect, 1)

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    MainClass().main()
