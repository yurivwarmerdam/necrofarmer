import pygame as pg
from pytmx import util_pygame
from math import floor

from scripts.tilemap import TileData, Tile
from pygame.math import Vector2
from pprint import pprint

pg.display.set_mode((50, 50))
tmx_data = util_pygame.load_pygame("tilemaps/another_island.tmx")
# tmx_a = util_pygame.load_pygame("tilemaps/another_island.tmx", load_all_tiles=True)
named_tiledata = {}
properties_dict = tmx_data.tile_properties
isometric = tmx_data.orientation == "isometric"
for gid in properties_dict.keys():
    if "name" in properties_dict[gid]:
        tileset = tmx_data.get_tileset_from_gid(gid)
        offset = -(
            Vector2(tileset.offset)
            + (-floor(tmx_data.tilewidth / 2), floor(tmx_data.tileheight / 2))
        )
        name = properties_dict[gid]["name"]
        tile = Tile  # TBD
        size = Vector2(tmx_data.tileheight, tmx_data.tilewidth)
        properties = properties_dict[gid]
        surf = tmx_data.get_tile_image_by_gid(gid)

        named_tiledata[name] = TileData(
            Tile,  # TBD
            Vector2(0, 0),
            size,
            properties,
            surf,
            offset,
            isometric,
        )

pprint(named_tiledata.keys())
