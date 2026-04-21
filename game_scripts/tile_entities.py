import pygame as pg
from pytmx.util_pygame import load_pygame


class TileEntities:
    def __init__(self, tmx_file="tilemaps/tile_entities.tmx") -> None:
        tmx_data = load_pygame(tmx_file)
        entity_layer = tmx_data.layers[0]
        self.data = entity_layer.data
        for tile in self.data:


def tranform_subtiles(tile_idxs,pos):
    # TODO: not done.
    return [idx + tile_idxs for idx in tile_idxs]

if __name__ == "__main__":
    pg.init()
    display = pg.display.set_mode((0, 0), pg.RESIZABLE)
    tile_entities = TileEntities()
    print(tile_entities.data)
