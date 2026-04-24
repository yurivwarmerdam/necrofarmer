import pygame as pg
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from math import floor


class TileEntities:
    def __init__(self, tmx_file="tilemaps/tile_entities.tmx") -> None:
        self.tiles = {}

        tmx_data = load_pygame(tmx_file)
        tmx_layer = tmx_data.layers[0]  # entity_layer
        self.data = tmx_layer.data
        half_w = floor(tmx_data.tilewidth / 2)
        half_h = floor(tmx_data.tileheight / 2)
        for x, y, surf in tmx_layer.tiles():
            pytmx_gid = self.data[y][x]
            tileset = tmx_data.get_tileset_from_gid(pytmx_gid)

            tile_properties = tmx_data.get_tile_properties_by_gid(pytmx_gid)
            name = tile_properties["name"]
            offset = -(Vector2(tileset.offset) + (-half_w, half_h))
            print(pytmx_gid, type(pytmx_gid))
            print(surf, type(surf))
            print(tile_properties, type(tile_properties))
            print(offset, type(offset))
            1 / 0
            self.tiles[name] = (
                surf,
                tile_properties,
                offset,
            )


def tranform_subtiles(tile_idxs, pos):
    # TODO: not done.
    return [idx + tile_idxs for idx in tile_idxs]


if __name__ == "__main__":
    pg.init()
    display = pg.display.set_mode((0, 0), pg.RESIZABLE)
    tile_entities = TileEntities()
    print(tile_entities.tiles)
