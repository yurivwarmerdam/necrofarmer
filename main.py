import sys
import pygame as pg
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from scripts.entities import PlayerEntity, Seed, BTGroup
from scripts.skeleton import Skeleton
from scripts.utils import load_image
from scripts.tilemap import Tilemap
from scripts.ui import ManaBar

asd = "asd!"


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
            self,
            "player",
            Vector2(50, 50),
            self.assets["wizard"].get_size(),
            self.assets["wizard"],
        )

        self.seeds = Group(
            Seed(self, self.assets["seed"], Vector2(200, 300)),
        )

        self.skeletons = BTGroup(
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(300, 300)
            ),
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(280, 280)
            ),
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(280, 200)
            ),
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(200, 300)
            ),
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(250, 310)
            ),
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(330, 320)
            ),
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(310, 340)
            ),
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(325, 317)
            ),
        )

        self.ui = Group(ManaBar(self))

        self.tilemap = Tilemap("art/tmx/field.tmx", ["ground", "plants and graves"])

        print("---")

        self.TREE_EVENT = pg.USEREVENT + 1
        pg.time.set_timer(self.TREE_EVENT, 1000)

    def main(self):
        while True:
            _delta = self.clock.get_time() / 1000.0

            self.handle_events()
            self.handle_key_input()

            # update entities
            self.update_all(_delta)

            self.draw_all()

            # redraws frame
            self.screen.blit(
                pg.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pg.display.update()
            self.clock.tick(60)

    def handle_events(self):
        # Input stuff and quit boilerplate. Consider moving quit to generic outer loop.
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_F8
            ):
                self.quit()
            if event.type == self.TREE_EVENT:
                self.skeletons.tick()
                print("Custom event triggered!")
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.player.action()

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
        # TODO: What's with those flip thing, anyway?
        # fill bg
        self.display.fill((14, 64, 128))
        # draw bg
        self.tilemap.get_layer("ground").draw(self.display)
        # draw entities
        self.seeds.draw(self.display)
        self.skeletons.draw(self.display)
        self.tilemap.get_layer("plants and graves").draw(self.display)
        self.player.render(self.display)
        self.ui.draw(self.display)

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    MainClass().main()
