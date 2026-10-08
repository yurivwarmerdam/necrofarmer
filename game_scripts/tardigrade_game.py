import pygame as pg

from game_scripts.commander import get_commander
from game_scripts.cursor import Cursor
from game_scripts.tardigrade import Tardigrade
from game_scripts.thopter import Thopter
from scripts.game import Game
from game_scripts import star
from scripts.group_server import get_group_server
from game_scripts.spawner import get_spawner
from game_scripts.game_tilemap import get_tilemap
from game_scripts.ui.main_ui import MainUI
from pygame.math import Vector2

BTREE_EVENT = pg.USEREVENT + 999


class TardigradeGame(Game):
    def __init__(self) -> None:
        resolution = (636, 333)
        super().__init__(resolution)

        self.ui = MainUI()

        tilemap = get_tilemap("tilemaps/another_island.tmx")
        star.get_star_server(tilemap)

        self.group_server.add_render_groups(tilemap.layers)

        # spawner = get_spawner()

        Cursor()
        self.commander = get_commander()
        # why doesn't commander do this inside init?
        self.commander.box.add(self.group_server.draw)

        pg.time.set_timer(BTREE_EVENT, 100)

        # -----------------------------

        Tardigrade(pg.Vector2(150, 120))
        Tardigrade(Vector2(120, 150))
        Tardigrade(Vector2(150, 150))

        Thopter(Vector2(200, 200))

        # tilemap.spawn_tile_str("sawmill", Vector2(96, 130), "active")

    def handle_camera_move(self):
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

    def process_events(self, events):
        for event in events:
            if event.type == BTREE_EVENT:
                self.group_server.behavior_trees.tick()
                continue  # This was break. You know what you did.
            elif event.type == pg.VIDEORESIZE:
                self.camera.set_window_resolution(event.size)
                self.ui_manager.set_window_resolution(event.size)
            elif event.type == pg.KEYDOWN:
                # this all wants to be camera.process_events()
                # Also: camera zoom does not properly handle mouse pos rescaling.
                if event.key == pg.K_1:
                    self.camera.set_zoom(1)
                elif event.key == pg.K_2:
                    self.camera.set_zoom(2)
                elif event.key == pg.K_3:
                    self.camera.set_zoom(3)
                elif event.key == pg.K_4:
                    self.camera.set_zoom(4)
            processed = False
            processed = self.ui_manager.process_events(event)

            if not processed:
                processed = self.commander.process_events(event)

        pass

    def update(self, delta):
        super().update(delta)
        camera_move = self.handle_camera_move()
        if camera_move != Vector2(0, 0):
            self.camera.pos += camera_move
        self.ui.update(delta)
        pass


if __name__ == "__main__":
    game = TardigradeGame()
    game.main()
