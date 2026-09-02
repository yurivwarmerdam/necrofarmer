import pygame as pg
from pytmx import util_pygame
from math import floor

from scripts.tilemap import TileData, Tile
from pygame.math import Vector2
from pprint import pprint

pg.display.set_mode((50, 50))
tmx = util_pygame.load_pygame("tilemaps/another_island.tmx")
# tmx_a = util_pygame.load_pygame("tilemaps/another_island.tmx", load_all_tiles=True)
named_tiledata = {}
properties_dict = tmx.tile_properties
for gid in properties_dict.keys():
    if "name" in properties_dict[gid]:
        name = properties_dict[gid]["name"]
        tile = Tile  # TBD
        size = Vector2(tmx.tileheight, tmx.tilewidth)
        properties = properties_dict[gid]
        surf = tmx.get_tile_image_by_gid(gid)
        tileset = tmx.get_tileset_from_gid(gid)
        offset = -(
            Vector2(tileset.offset)
            + (-floor(tmx.tilewidth / 2), floor(tmx.tileheight / 2))
        )
        isometric = tmx.orientation == "isometric"

        named_tiledata[name] = TileData(
            Tile,  # TBD
            Vector2(0, 0),
            size,
            properties,
            surf,
            offset,
            isometric,
        )

print(named_tiledata)

# Map GID to a tuple of (Surface, properties dict)
# tile_set = {
#     (tmx.get_tile_image_by_gid(gid), props)
#     for gid, props in tmx.tile_properties.items()
# }
# print(tile_set)
