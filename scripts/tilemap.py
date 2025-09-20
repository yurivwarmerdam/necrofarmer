from pygame.sprite import Group, LayeredUpdates
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from pygame import Vector2
from math import floor
from scripts.custom_sprites import NodeSprite


class Tile(NodeSprite):
    def __init__(
        self,
        pos,
        image,
        properties: dict,
        *groups,
        anchor="bottomleft",
        offset=Vector2(0, 0),
    ):
        super().__init__(image, pos, anchor, offset, *groups)
        self.properties: dict = properties if properties else {}

    def has(self, attribute):
        return attribute in self.properties


class Tilemap:
    """
    Generic Tilemap. Holds several layers of Sprite Groups.
    Args:
        tmx_file: filename to load tilemap from
    """

    def __init__(
        self,
        tmx_file,
        # TODO: Group mappings should probably be removed
        # and instead be handled by wiring together outside of this class
        # group_mappings: dict[str, Group],
    ):
        self.tmx_data: TiledMap = load_pygame(tmx_file)
        self.layers = {}
        self.map = {}

        self.isometric = self.tmx_data.orientation == "isometric"

        # TODO: we are here atm:
        for layer in self.tmx_data.visible_layers:
            name = layer.name
            self.map[name] = [
                [None for _ in range(self.tmx_data.height)]
                for _ in range(self.tmx_data.width)
            ]
            if hasattr(layer, "data"):
                self.make_layer(layer, name)

    def make_layer(self, tmx_layer, name):
        
        if tmx_layer.properties.get("LayeredUpdates", False):
            layer = LayeredUpdates()
        else:
            layer = Group()
        # group = Group()

        self.layers[name] = layer
        half_w = floor(self.tmx_data.tilewidth / 2)
        half_h = floor(self.tmx_data.tileheight / 2)
        for x, y, surf in tmx_layer.tiles():
            world_pos = self.map_to_world(x, y)
            pytmx_gid = tmx_layer.data[y][x]  # Warning: y x != x y
            tileset = self.tmx_data.get_tileset_from_gid(pytmx_gid)
            offset = -(Vector2(tileset.offset) + (-half_w, half_h))
            tile_properties = self.tmx_data.get_tile_properties_by_gid(pytmx_gid)
            tile_properties = self.tmx_data.get_tile_properties_by_gid(pytmx_gid)

            self.map[name][x][y] = Tile(
                world_pos,
                surf,
                tile_properties,
                layer,
                offset=offset,
            )

    def get_layer(self, layer):
        return self.layers[layer]

    def get_neigbors(self, tile_pos, distance=1):
        result = []
        for x in range(-distance, distance):
            for y in range(-distance, distance):
                if (x, y) == tile_pos:
                    continue
                result.append((x, y))
        return result

    def get_tile(self, layer: str, pos: Vector2):
        return self.map[layer][floor(pos.x)][floor(pos.y)]

    def kill_tile(self, layer: str, pos: Vector2):
        tile = self.map[layer][floor(pos.x)][floor(pos.y)]
        tile.kill
        self.map[layer][floor(pos.x)][floor(pos.y)] = None
        self.layers[layer].remove(tile)

    def add_tile(self, layer:str, map_pos:Vector2):
        
        pass

    def tile_properties(self, layer: str, pos: Vector2):
        return self.get_tile(layer, pos).properties

    def get_tile_idxs_by_property(self, property, layer) -> list[Vector2]:
        return [
            Vector2(x, y)
            for x, row in enumerate(self.map[layer])
            for y, cell in enumerate(row)
            if cell is not None and property in cell.properties
        ]

    def get_tiles_by_property(self, property, layer) -> list:
        tiles = [
            tile for tile in iter(self.old_layers[layer]) if property in tile.properties
        ]
        return tiles

    def get_tile_attrs(self, tile, layer) -> dict:
        return self.map[layer][tile].properties

    def set_tile(self, pos: Vector2, layer: str, tile: Tile):
        self.old_layers[layer][pos.x][pos.y] = tile

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
        return self.map_to_world(map_pos.x, map_pos.y)
