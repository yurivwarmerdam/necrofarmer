from math import floor

from pygame import Vector2
from pytmx.pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from scripts.tilemap.tile import Tile
from scripts.tilemap.tiledata import TileData


# On get or create AND on register named tiles: make named tiledata
# but only when items are present in both tmx and named tiles.


class TmxParser:
    # TODO: add feature to have named tiles based on a tilemap index
    # instead of a name property
    def __init__(self) -> None:
        self.tmx: dict[str, TiledMap] = {}
        self.named_tiles: dict[str, type[Tile]] = {}
        self.named_data: dict[str, TileData] = {}

    def register_named_tiles(
        self, named_tiles: dict[str, type[Tile]]
    ) -> dict[str, TileData]:
        """
        Register tiles with a name property.
        This will allow looking up an associated class that inherits from Tile.
        The generated tiledata is stored in named_data and all stored_data si returned
        """
        self.named_tiles.update(named_tiles)
        self._make_named_tiledata()
        return self.named_data

    def get_or_create(self, filename: str):
        if not self.tmx.get(filename):
            self.tmx[filename] = load_pygame(filename)
        self._make_named_tiledata()
        return self.tmx[filename]

    def _make_named_tiledata(self) -> None:
        # named_tiledata = {}
        for tmx_map in self.tmx.values():
            properties_dict = tmx_map.tile_properties
            isometric = tmx_map.orientation == "isometric"
            for gid in properties_dict.keys():
                if "name" in properties_dict[gid]:
                    tileset = tmx_map.get_tileset_from_gid(gid)
                    offset = -(
                        Vector2(tileset.offset)
                        + (
                            -floor(tmx_map.tilewidth / 2),
                            floor(tmx_map.tileheight / 2),
                        )
                    )
                    name = properties_dict[gid]["name"]
                    tile = self.named_tiles.get(name, Tile)  # TBD
                    size = Vector2(tmx_map.tilewidth, tmx_map.tileheight)
                    properties = properties_dict[gid]
                    surf = tmx_map.get_tile_image_by_gid(gid)

                    self.named_data[name] = TileData(
                        tile,
                        Vector2(0, 0),
                        size,
                        properties,
                        surf,
                        offset,
                        isometric,
                    )


_instance = None


# TODO: how to deal with re-instantiating tilemap on load, level change, map expansion, whatever.
def get_tmx_parser(tmx_path: str | None = None) -> TmxParser:
    global _instance
    if _instance is None:
        _instance = TmxParser()
    return _instance
