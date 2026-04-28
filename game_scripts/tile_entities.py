import pygame as pg
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from math import floor
from scripts.tilemap import TileDataLayers
from pytmx.map import TiledMap, TiledLayer

bigtile_entities = {
    "sawmill": bigtiles.Sawmill,
    "thopter_factory_2": bigtiles.ThopterFactory,
}

class TileEntitites():
    def __init__(self) -> None:
        self.entities=TileDataLayers("tilemaps/tile_entities.tmx",bigtile_entities).layers["tile_entities"]




if __name__ == "__main__":
    pg.init()
    display = pg.display.set_mode((0, 0), pg.RESIZABLE)
    te=TileEntitites
    print(te.)
