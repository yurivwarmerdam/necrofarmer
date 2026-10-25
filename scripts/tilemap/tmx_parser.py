from math import floor

from pygame import Vector2
from pytmx.pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from scripts.tilemap.tile import Tile
from scripts.tilemap.tiledata import TileData


class TmxParser:
    def __init__(self, tmx_file, typed_tiles: dict[str, type[Tile]]) -> None:
        self.tmx_data: TiledMap = load_pygame(tmx_file)
        self.named_tiledata = self.make_named_tiledata(typed_tiles)
        pass

    def make_named_tiledata(
        self, typed_tiles: dict[str, type[Tile]]
    ) -> dict[str, TileData]:
        named_tiledata = {}
        properties_dict = self.tmx_data.tile_properties
        isometric = self.tmx_data.orientation == "isometric"
        for gid in properties_dict.keys():
            if "name" in properties_dict[gid]:
                tileset = self.tmx_data.get_tileset_from_gid(gid)
                offset = -(
                    Vector2(tileset.offset)
                    + (
                        -floor(self.tmx_data.tilewidth / 2),
                        floor(self.tmx_data.tileheight / 2),
                    )
                )
                name = properties_dict[gid]["name"]
                tile = typed_tiles.get(name, Tile)  # TBD
                size = Vector2(self.tmx_data.tilewidth, self.tmx_data.tileheight)
                properties = properties_dict[gid]
                surf = self.tmx_data.get_tile_image_by_gid(gid)

                named_tiledata[name] = TileData(
                    tile,
                    Vector2(0, 0),
                    size,
                    properties,
                    surf,
                    offset,
                    isometric,
                )
        return named_tiledata
