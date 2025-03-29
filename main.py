import sys
import pygame as pg
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from scripts.entities import PlayerEntity, Skeleton, Seed
from scripts.utils import load_image  # , sheet_to_sprite
from scripts.tilemap import Tilemap
from scripts.ui import ManaBar
from simple_bt.build import simple_run_bind
from threading import Thread

from time import sleep

asd = "asd!"


def sleeper():
    print(f"starting sleep{asd}")
    1/0
    sleep(0.5)
    print("ending sleep")


def output_dummy() -> int:
    """Simulates returning a value such as a move target"""
    return 1


def parameter_sleeper(value: int):
    print(f"My param is: {value}! Time to sleep")
    sleep(0.5)
    print("ending sleep")


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

        self.skeletons = Group(
            Skeleton(
                self, self.assets["skeleton"], self.player, Tilemap, Vector2(300, 300)
            ),
            # Skeleton(
            #     self, self.assets["skeleton"], self.player, Tilemap, Vector2(280, 280)
            # ),
            # Skeleton(
            #     self, self.assets["skeleton"], self.player, Tilemap, Vector2(280, 200)
            # ),
            # Skeleton(
            #     self, self.assets["skeleton"], self.player, Tilemap, Vector2(200, 300)
            # ),
            # Skeleton(
            #     self, self.assets["skeleton"], self.player, Tilemap, Vector2(250, 310)
            # ),
            # Skeleton(
            #     self, self.assets["skeleton"], self.player, Tilemap, Vector2(330, 320)
            # ),
            # Skeleton(
            #     self, self.assets["skeleton"], self.player, Tilemap, Vector2(310, 340)
            # ),
            # Skeleton(
            #     self, self.assets["skeleton"], self.player, Tilemap, Vector2(325, 317)
            # ),
        )

        self.ui = Group(ManaBar(self))

        self.tilemap = Tilemap("art/tmx/field.tmx", ["ground", "plants and graves"])
        # print(self.tilemap.layers["ground"].sprites())

        print("---")
        # thread = Thread(target=simple_run_bind.test_func, args=[sleeper])
        # thread.start()

        # # simple_run_bind.simple_run()
        # thread = Thread(target=simple_run_bind.simple_run)
        # thread.start()

        builder = simple_run_bind.PyTreeBuilder(
            sleeper, output_dummy, parameter_sleeper
        )
        print("---")
        
        builder.tick_tree()
        print("---")
        # print("asddef")

    def main(self):
        while True:
            # deltatime
            _delta = self.clock.get_time()
            # fill bg
            self.display.fill((14, 64, 128))
            # Input stuff and quit boilerplate. Consider moving quit to generic outer loop.
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_F8
                ):
                    self.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.player.action()
            # ----------main body------------#
            self.handle_key_input()

            pg.draw.rect(self.display, (40, 40, 40), self.collision_obstacle)

            # update entities
            self.update_all()

            self.draw_all()

            player_collision = pg.Rect(*self.player.pos, *self.player.size)
            if player_collision.colliderect(self.collision_obstacle):
                pg.draw.rect(self.display, (150, 20, 20), player_collision, 1)

            # ----------/main body------------#
            # redraws frame
            self.screen.blit(
                pg.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pg.display.update()
            self.clock.tick(60)

    def handle_key_input(self):
        self.keys_pressed = pg.key.get_pressed()
        self.movement = Vector2(0, 0)
        self.movement.x = self.keys_pressed[pg.K_RIGHT] - self.keys_pressed[pg.K_LEFT]
        self.movement.y = self.keys_pressed[pg.K_DOWN] - self.keys_pressed[pg.K_UP]

    def update_all(self):
        self.player.update(self.movement, self.keys_pressed)
        self.seeds.update()
        self.skeletons.update()
        self.ui.update()

    def draw_all(self):
        # draw bg
        # self.tilemap.render(self.display)
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
