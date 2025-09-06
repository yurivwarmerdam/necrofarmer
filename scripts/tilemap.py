from pygame.sprite import Sprite, Group
from pytmx.util_pygame import load_pygame, TiledMap
from pygame import Vector2
from math import floor


class Tile(Sprite):
    def __init__(self, pos, image, tile_properties: dict, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(bottomleft=pos)
        self.properties: dict = tile_properties if tile_properties else {}

    def has(self, attribute):
        return attribute in self.properties


class Tilemap:
    """
    Generic Tilemap. Holds several layers of Sprite Groups.
    Args:
        tmx_file: filename to load tilemap from
        group_mappings: dict containing layer names ot load from the tilemaps (keys), paired with their corresponding render group
    """

    def __init__(
        self,
        tmx_file,
        # TODO: Group mappings should probably be removed
        # and instead be handled by wiring together outside of this class
        group_mappings: dict[str, Group],
    ):
        self.tmx_data:TiledMap = load_pygame(tmx_file)
        self.layers = {}
        self.map = {}

        self.isometric = self.tmx_data.orientation == "isometric"

        tmx_layers = list(self.tmx_data.visible_layers)

        # iterate all groups
        for group_name in group_mappings:
            self.layers[group_name] = Group()

            # instantiate empty map for layer
            self.map[group_name] = [
                [None for _ in range(self.tmx_data.height)]
                for _ in range(self.tmx_data.width)
            ]
            tmx_layer = next(
                (layer for layer in tmx_layers if layer.name == group_name), None
            )
            if tmx_layer and hasattr(tmx_layer, "data"):
                self.make_layer_tiles(tmx_layer, group_name, group_mappings[group_name])

    def make_layer_tiles(self, tmx_layer, group_name, group):
        half_w = floor(self.tmx_data.tilewidth / 2)
        half_h = floor(self.tmx_data.tileheight / 2)
        for x, y, surf in tmx_layer.tiles():
            world_pos = self.map_to_world(x, y)
            pytmx_gid = tmx_layer.data[y][x]  # Warning: y x != x y
            tileset = self.tmx_data.get_tileset_from_gid(pytmx_gid)
            offset_pos = world_pos + tileset.offset + (-half_w, half_h)
            tile_properties = self.tmx_data.get_tile_properties_by_gid(pytmx_gid)
            tile_properties = self.tmx_data.get_tile_properties_by_gid(pytmx_gid)
            self.map[group_name][x][y] = Tile(
                offset_pos, surf, tile_properties, self.layers[group_name], group
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

    def tile(self, layer: str, pos: Vector2):
        return self.map[layer][pos.x][pos.y]

    def tile_properties(self, layer: str, pos: Vector2):
        return self.tile(layer, pos).properties

    def get_tiles_by_attr(self, attribute, layer) -> list:
        tiles = [tile for tile in iter(self.layers[layer]) if tile.has(attribute)]
        return tiles

    def get_tile_attrs(self, tile, layer) -> dict:
        return self.map[layer][tile].properties

    def set_tile(self, tile_pos, layer: str, tile_id=0):
        # TODO
        pass

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
