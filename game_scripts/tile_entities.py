import pygame as pg
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from math import floor
from scripts.tilemap import TileData, Tile, map_to_world
from pytmx.map import TiledMap, TiledLayer


class TileDataLayers:
    def __init__(
        self,
        tmx_data: TiledMap | str,
        tile_types: dict[str, type[Tile]] = {},
    ):
        """
        container object for layer of TileData.
        params:
        tmx_data: Preloaded tmx data. If a string is supplied it is extracted, instead.
        tile_types: optional dict of custyom tile types. Any types not recognized will default to specifying Tile.
        """
        if isinstance(tmx_data, str):
            tmx_data = load_pygame(tmx_data)
        self.tmx_data = tmx_data
        self.tile_types = tile_types
        self.tile_size = Vector2(tmx_data.tilewidth, tmx_data.tileheight)
        self.isometric = self.tmx_data.orientation == "isometric"

        self.layers: dict[str, dict[Vector2, TileData]] = {}

        # tmx_data = load_pygame(tmx_file)
        for source_layer in tmx_data.visible_layers:
            if hasattr(source_layer, "data"):
                self.layers[source_layer.name] = self.make_layerdata(source_layer)

    def make_layerdata(self, source_layer: TiledLayer) -> dict[Vector2, TileData]:
        layer = {}
        for x, y, surf in source_layer.tiles():
            tile = self.make_tiledata(layer, x, y, surf)
            layer[Vector2(x, y)] = tile
        return layer

    def make_tiledata(self, tmx_layer, x, y, surf):
        pytmx_gid = tmx_layer.data[y][x]  # Warning: y x != x y
        tileset = self.tmx_data.get_tileset_from_gid(pytmx_gid)
        offset = -(
            Vector2(tileset.offset)
            + (-floor(self.tmx_data.tilewidth / 2), floor(self.tmx_data.tileheight / 2))
        )
        properties: dict = self.tmx_data.get_tile_properties_by_gid(pytmx_gid) or {}
        tile_type = self.tile_types.get(properties.get("name", ""), Tile)
        return TileData(
            tile_type=tile_type,
            map_pos=Vector2(x, y),
            world_pos=map_to_world(
                x, y, self.tile_size.x, self.tile_size.y, self.isometric
            ),
            properties=properties,
            surf=surf,
            offset=offset,
        )



if __name__ == "__main__":
    pg.init()
    display = pg.display.set_mode((0, 0), pg.RESIZABLE)
    tile_entities = TileDataLayers("tilemaps/tile_entities.tmx")
    print(tile_entities.tiles)
