import pygame as pg
pg.display.set_mode((50,50))
from pytmx import util_pygame
tmx =util_pygame.load_pygame("tilemaps/another_island.tmx")
tmx_a =util_pygame.load_pygame("tilemaps/another_island.tmx",load_all_tiles=True)
from pprint import pprint
from scripts.tilemap import TileData,Tile
from pygame.math import Vector2
from math import floor

named_tiledata={}
properties_dict=tmx.tile_properties
for gid in properties_dict.keys():
    if "name" in tmx.tile_properties[gid]:
        name=named_tiledata[properties_dict[gid]["name"]]
        tile=Tile # TBD
        size=Vector2(tmx.tileheight,tmx.tilewidth)
        properties=properties_dict[gid]
        surf=tmx.get_tile_image_by_gid(gid)
        tileset=tmx.get_tileset_from_gid(gid)
        offset=-(
            Vector2(tileset.offset)
            + (-floor(tmx.tilewidth / 2), floor(tmx.tileheight / 2))
        )
        isometric= tmx.orientation == "isometric"

for id in named_tiles.keys():
    TileData(Tile,Vector2(0,0),Vector2(tmx.tilewidth,tmx.tileheight),named_tiles[id],tmx.get_tile_image_by_gid)

print(named_tiles)
# Map GID to a tuple of (Surface, properties dict)
# tile_set = {
#     (tmx.get_tile_image_by_gid(gid), props)
#     for gid, props in tmx.tile_properties.items()
# }
# print(tile_set)