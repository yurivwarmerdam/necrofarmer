import pygame as pg

from game_scripts.tardigrade import Tardigrade
from game_scripts.thopter import Thopter
from scripts.game import Game
from game_scripts import star
from scripts.group_server import get_group_server
from game_scripts.spawner import get_spawner
from game_scripts.game_tilemap import get_tilemap
from game_scripts.ui.main_ui import MainUI

class TardigradeGame(Game):
    def __init__(self) -> None:
        resolution = (636, 333)
        super().__init__(resolution)

        ui = MainUI()

        tilemap = get_tilemap("tilemaps/another_island.tmx")
        star.get_star_server(tilemap)

        group_server = get_group_server()
        group_server.add_render_groups(tilemap.layers)
        # Should I add the following 2 groups as a core part of group server?
        group_server.add_render_groups({"front": Group()})
        group_server.add_render_groups({"draw": Group()})

        spawner = get_spawner()

        cursor = Cursor()
        commander = get_commander()
        commander.box.add(group_server.render_groups["draw"])

        BTREE_EVENT = pg.USEREVENT + 999
        pg.time.set_timer(BTREE_EVENT, 100)


        # -----------------------------


        Tardigrade(pg.Vector2(150, 120))
        Tardigrade(Vector2(120, 150))
        Tardigrade(Vector2(150, 150))

        Thopter(Vector2(200, 200))
        
        # tilemap.spawn_tile_str("sawmill", Vector2(96, 130), "active")

    def process_events(self, events):
        pass
