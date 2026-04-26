from math import floor

from pygame import Vector2
from pygame.sprite import AbstractGroup, Group, LayeredUpdates
from pytmx.map import TiledMap, TiledLayer
from pytmx.util_pygame import load_pygame

from scripts.custom_sprites import NodeSprite
from dataclasses import dataclass
from pygame.surface import Surface


# lol. Allows for weird notation
# some_tiledata.tile.type(some_tiledata)
@dataclass
class TileData:
    tile_type: type[Tile]
    map_pos: Vector2
    world_pos: Vector2
    properties: dict
    surf: Surface
    offset: Vector2
    anchor: str = "bottomleft"

    def make_tile(self):
        return self.tile_type(
            self.world_pos, self.surf, self.properties, offset=self.offset
        )


class Tile(NodeSprite):
    def __init__(self, Tiledata: TileData, *groups):
        super().__init__(
            Tiledata.surf, TileData.world_pos, Tiledata.anchor, Tiledata.offset, *groups
        )
        self.properties = Tiledata.properties

    def has(self, attribute):
        return attribute in self.properties


# class Tile(NodeSprite):
#     def __init__(
#         self,
#         pos,
#         image,
#         properties: dict,
#         *groups,
#         anchor="bottomleft",
#         offset=Vector2(0, 0),
#     ):
#         super().__init__(image, pos, anchor, offset, *groups)
#         self.properties: dict = properties if properties else {}

#     def has(self, attribute):
#         return attribute in self.properties


class TileDataLayers:
    # TODO: maybe implement __getItem__?
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


class Tilemap:
    """
    Generic Tilemap. Holds several layers of Sprite Groups.
    Args:
        tmx_file: filename to load tilemap from
    """

    def __init__(self, tmx_file):
        self.tmx_data: TiledMap = load_pygame(tmx_file)
        self.layers: dict[str, AbstractGroup] = {}
        # TODO: Map currently breaks when building a map with negative indexes. Fix this.
        self.map = {}

        # self.isometric = self.tmx_data.orientation == "isometric"
        tmx_data = load_pygame(tmx_file)
        self.tile_data_layers = TileDataLayers(tmx_data)

        for layer_name in self.tile_data_layers.layers:
            self.init_layer(layer_name)

        # for layer in self.tmx_data.visible_layers:
        #     name = layer.name
        #     self.map[name] = [
        #         [None for _ in range(self.tmx_data.height)]
        #         for _ in range(self.tmx_data.width)
        #     ]
        #     if hasattr(layer, "data"):
        #         self.make_layer(layer, name)

    def init_layer(self, layer_name):
        self.map[layer_name] = {}
        data_layer = self.tile_data_layers.layers[layer_name]
        for map_pos in data_layer:
            tile_data: TileData = data_layer[map_pos]
            tile = tile_data.tile_type(tile_data)
            self.set_tile(tile, layer_name, tile_data.map_pos)

    def populate_layer(self, layere_name):

        pass

    # def make_layer(self, tmx_layer, name):
    #     if tmx_layer.properties.get("LayeredUpdates", False):
    #         layer = LayeredUpdates()
    #     else:
    #         layer = Group()

    #     self.layers[name] = layer
    #     half_w = floor(self.tmx_data.tilewidth / 2)
    #     half_h = floor(self.tmx_data.tileheight / 2)
    #     for tile in tmx_layer.tiles():
    #         self.make_tiledata(tmx_layer, *tile)
    #         x, y, surf = tile
    #         pytmx_gid = tmx_layer.data[y][x]  # Warning: y x != x y
    #         tileset = self.tmx_data.get_tileset_from_gid(pytmx_gid)
    #         offset = -(Vector2(tileset.offset) + (-half_w, half_h))
    #         tile_properties = self.tmx_data.get_tile_properties_by_gid(pytmx_gid)

    #         tile = Tile(
    #             Vector2(0, 0),
    #             surf,
    #             tile_properties,
    #             offset=offset,
    #         )

    #         self.set_tile(tile, name, Vector2(x, y))

    def get_layer(self, layer_name):
        return self.layers[layer_name]

    def get_neigbors(self, tile_pos: Vector2, distance=1) -> list[Vector2]:
        result = []
        for x in range(-distance, distance + 1):
            for y in range(-distance, distance + 1):
                if x == 0 and y == 0:
                    continue
                candidate = tile_pos + Vector2(x, y)
                try:
                    next(iter(self.map.values()))[floor(candidate.x)][
                        floor(candidate.y)
                    ]
                    result.append(candidate)
                except IndexError:
                    continue
        return result

    def get_tilev(self, layer: str, pos: Vector2):
        try:
            return self.map[layer][floor(pos.x)][floor(pos.y)]
        except IndexError:
            pass

    def set_tile(self, tile: Tile, layer: str, map_pos: Vector2):
        self.layers[layer].add(tile)
        self.map[layer][map_pos] = tile

    def kill_tile(self, layer: str, pos: Vector2):
        tile = self.map[layer][floor(pos.x)][floor(pos.y)]
        tile.kill
        self.map[layer][floor(pos.x)][floor(pos.y)] = None
        self.layers[layer].remove(tile)

    def get_tile_idxs_by_property(self, property, layer) -> list[Vector2]:
        return [
            Vector2(x, y)
            for x, row in enumerate(self.map[layer])
            for y, cell in enumerate(row)
            if cell is not None and property in cell.properties
        ]

    def get_tiles_by_property(self, property, layer) -> list:
        tiles = [
            tile
            for tile in iter(self.layers[layer])
            if property in getattr(tile, "properties", {})
        ]
        return tiles

    def get_tilev_properties(self, tile: Vector2, layer: str) -> dict:
        """
        Returns a dict containing all custom properties for a tile.
        Returns an empty dict for unpopulated tiles.
        """
        return getattr(self.map[layer][floor(tile.x)][floor(tile.y)], "properties", {})

    def world_to_map(self, world_pos: Vector2) -> Vector2:
        if self.isometric:
            half_w = self.tmx_data.tilewidth / 2
            half_h = self.tmx_data.tileheight / 2
            x = (((world_pos.x / half_w) + (world_pos.y / half_h)) / 2) + 0.5
            y = (((world_pos.y / half_h) - (world_pos.x / half_w)) / 2) + 0.5
            return Vector2(floor(x), floor(y))
        else:
            return Vector2(
                floor(world_pos.x / self.tmx_data.tilewidth),
                floor(world_pos.y / self.tmx_data.tileheight),
            )

    def map_to_world(self, x, y) -> Vector2:
        if self.isometric:
            return Vector2(
                self.tmx_data.tilewidth / 2 * (x - y),
                self.tmx_data.tileheight / 2 * (x + y),
            )
        else:
            return Vector2(
                x * self.tmx_data.tilewidth,
                y * self.tmx_data.tileheight,
            )

    def map_to_worldv(self, map_pos: Vector2) -> Vector2:
        return self.map_to_world(floor(map_pos.x), floor(map_pos.y))


def map_to_world(x, y, tilewidth, tileheight, isometric=False):
    if isometric:
        return Vector2(
            tilewidth / 2 * (x - y),
            tileheight / 2 * (x + y),
        )
    else:
        return Vector2(
            x * tilewidth,
            y * tileheight,
        )


def map_to_worldv(map_pos: Vector2, tile_size: Vector2, isometric=False):
    return map_to_world(map_pos.x, map_pos.y, tile_size.x, tile_size.y, isometric)


def world_to_map(x, y, tilewidth, tileheight, isometric=False):
    if isometric:
        half_w = tilewidth / 2
        half_h = tileheight / 2
        x = (((x / half_w) + (y / half_h)) / 2) + 0.5
        y = (((y / half_h) - (x / half_w)) / 2) + 0.5
        return Vector2(floor(x), floor(y))
    else:
        return Vector2(
            floor(x / tilewidth),
            floor(y / tileheight),
        )


def world_to_mapv(world_pos: Vector2, tile_size: Vector2, isometric=False):
    return world_to_map(world_pos.x, world_pos.y, tile_size.x, tile_size.y, isometric)


if __name__ == "__main__":
    Tilemap("tilemaps/another_island.tmx")
