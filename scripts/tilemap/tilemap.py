from math import floor
from typing import override

from pygame import Vector2
from pygame.sprite import AbstractGroup, Group, LayeredUpdates, Sprite
from pytmx.map import TiledMap
from pytmx.util_pygame import load_pygame

from scripts.tilemap.tile import Tile, TileDataLayers
from scripts.tilemap.tiledata import TileData
from scripts.tilemap.tmx_parser import get_tmx_parser


class Tilemap(AbstractGroup):
    """
    Generic Tilemap. Holds several layers of Sprite Groups.
    Args:
        tmx_file: filename to load tilemap from
        typed_tiles: used for any tile with a "name" property
    """

    def __init__(
        self,
        tmx_file,
        typed_tiles: dict[str, type[Tile]] = {},
    ):
        super().__init__()
        self.tmx_data: TiledMap = get_tmx_parser().get_or_create(tmx_file)
        self.layers: dict[str, AbstractGroup] = {}

        # map has structure map[layer][(x,y)]
        # cannot use Vector for the x,y coords, becasue Vectors are unhashable, so tuples are used.
        self.map: dict[str, dict[tuple[int, int], Tile]] = {}

        tmx_data = load_pygame(tmx_file)
        self.isometric = self.tmx_data.orientation == "isometric"

        self.named_tiledata: dict[str, TileData] = get_tmx_parser().register_named_tiles(typed_tiles)
        print(self.named_tiledata.keys())
        self.tile_data_layers = TileDataLayers(tmx_data, typed_tiles)

        for layer_name in self.tile_data_layers.layers:
            self.init_layer(layer_name)

    @override
    def remove_internal(self, sprite: Sprite) -> None:
        # TODO: This is slow. Perhaaaaps the layers should actually take care of this?
        # They already know if a tile is in the layer; that's the definition!
        # also... allows me to remove map from the tilemap, and move it to a tilemaplayer, instead.
        super().remove_internal(sprite)

        for layer in self.map.values():
            if sprite in layer.values():
                for key in [k for k, v in layer.items() if v == sprite]:
                    del layer[key]

    # def make_named_tiledata(
    #     self, typed_tiles: dict[str, type[Tile]]
    # ) -> dict[str, TileData]:
    #     named_tiledata = {}
    #     properties_dict = self.tmx_data.tile_properties
    #     isometric = self.tmx_data.orientation == "isometric"
    #     for gid in properties_dict.keys():
    #         if "name" in properties_dict[gid]:
    #             tileset = self.tmx_data.get_tileset_from_gid(gid)
    #             offset = -(
    #                 Vector2(tileset.offset)
    #                 + (
    #                     -floor(self.tmx_data.tilewidth / 2),
    #                     floor(self.tmx_data.tileheight / 2),
    #                 )
    #             )
    #             name = properties_dict[gid]["name"]
    #             tile = typed_tiles.get(name, Tile)  # TBD
    #             size = Vector2(self.tmx_data.tilewidth, self.tmx_data.tileheight)
    #             properties = properties_dict[gid]
    #             surf = self.tmx_data.get_tile_image_by_gid(gid)

    #             named_tiledata[name] = TileData(
    #                 tile,
    #                 Vector2(0, 0),
    #                 size,
    #                 properties,
    #                 surf,
    #                 offset,
    #                 isometric,
    #             )
    #     return named_tiledata

    def init_layer(self, layer_name):
        self.map[layer_name] = {}
        if self.tmx_data.layernames[layer_name].properties.get("LayeredUpdates", False):
            layer = LayeredUpdates()
        else:
            layer = Group()
        self.layers[layer_name] = layer

        data_layer = self.tile_data_layers.layers[layer_name]
        for map_pos in data_layer:
            tile_data: TileData = data_layer[map_pos]
            if self.can_spawn_tile(tile_data, layer_name):
                self.spawn_tile(tile_data, layer_name)

    # TODO: Everything neighbor-related wants to be in utils
    def get_neighbors(self, tile_pos: Vector2, distance=1) -> list[Vector2]:
        result = []
        for x in range(-distance, distance + 1):
            for y in range(-distance, distance + 1):
                if x == 0 and y == 0:
                    continue
                candidate = tile_pos + Vector2(x, y)
                try:
                    next(iter(self.map.values()))[
                        floor(candidate.x), floor(candidate.y)
                    ]
                    result.append(candidate)
                except KeyError:
                    continue
        return result

    def get_tile(self, layer: str, x, y) -> Tile | None:
        try:
            return self.map[layer][x, y]
        except KeyError:
            pass

    def get_tilev(self, layer: str, pos: Vector2) -> Tile | None:
        return self.get_tile(layer, floor(pos.x), floor(pos.y))

    def spawn_tile(self, tile_data: TileData, layer_name: str):
        """creatues new tile from TileData"""
        new_tile = tile_data.tile_type(tile_data)
        if not self.set_tile_in_map(new_tile, layer_name, tile_data.map_pos):
            print(
                "erroneous tile placement! This an unwanted state? Killing the newborn."
            )
            new_tile.kill()

    def can_spawn_tile(self, tile_data: TileData, layer: str) -> bool:
        map_pos = tile_data.map_pos
        return self.map[layer].get((floor(map_pos.x), floor(map_pos.y)), None) is None

    def spawn_tile_str(self, tile_data_name: str, world_pos, layer):
        # TODO: How do I spawn something simple like grass?
        map_pos = self.world_to_map(world_pos)
        new_tiledata = self.named_tiledata[tile_data_name].move(map_pos)
        if self.can_spawn_tile(new_tiledata, layer):
            self.spawn_tile(new_tiledata, layer)

    def set_tile_in_map(self, tile: Tile, layer: str, map_pos: Vector2) -> bool:
        self.add(tile)
        self.layers[layer].add(tile)
        self.map[layer][floor(map_pos.x), floor(map_pos.y)] = tile
        return True

    def get_tile_idxs_by_property(
        self, property, layer_name, property_value=None
    ) -> list[tuple[int, int]]:
        return [
            cell
            for cell in self.map[layer_name]
            if self.map[layer_name][cell] is not None
            and property in self.map[layer_name][cell].properties
            and (
                property_value is None
                or self.map[layer_name][cell].properties[property] == property_value
            )
        ]

    def get_tiles_by_property(self, property, layer) -> list:
        tiles = [
            tile
            for tile in iter(self.layers[layer])
            if property in getattr(tile, "properties", {})
        ]
        return tiles

    def get_tile_properties(self, x: int, y: int, layer: str):
        try:
            return self.map[layer][floor(x), floor(y)].properties
        except KeyError:
            return {}

    def get_tilev_properties(self, tile: Vector2, layer: str) -> dict:
        """
        Returns a dict containing all custom properties for a tile.
        Returns an empty dict for unpopulated tiles.
        """
        return self.get_tile_properties(floor(tile.x), floor(tile.y), layer)

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
