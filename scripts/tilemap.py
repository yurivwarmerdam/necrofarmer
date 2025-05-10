import pygame as pg
from pygame.sprite import Sprite, Group
from pytmx.util_pygame import load_pygame
from pygame import Vector2
from math import floor


class Tile(Sprite):
    def __init__(self, pos, image, tile_properties: dict, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.properties: dict = tile_properties if tile_properties else {}

    def has(self, attribute):
        return attribute in self.properties


class Tilemap:
    """Generic Tilemap. Holds several layers of Sprite Groups."""

    def __init__(self, tmx_file, groups):
        self.tmx_data = load_pygame(tmx_file)
        self.groups = {}
        self.map = {}

        for group in groups:
            self.groups[group] = Group()
            self.map[group] = [
                [None for _ in range(self.tmx_data.height)]
                for _ in range(self.tmx_data.width)
            ]
        for layer in self.tmx_data.visible_layers:
            if layer.name in groups and hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = self.map_to_world(x, y)
                    gid = layer.data[y][x]  # Warning: y x != x y
                    tile_properties = self.tmx_data.get_tile_properties_by_gid(gid)
                    self.map[group][x][y] = Tile(
                        pos, surf, tile_properties, self.groups[layer.name]
                    )

    def get_layer(self, layer):
        return self.groups[layer]

    def get_neigbors(pos, distance=1):
        result = []
        for x in range(-distance, distance):
            for y in range(-distance, distance):
                if (x, y) == pos:
                    continue
                result.append((x, y))
        return result

    def tile(self, layer: str, pos: Vector2):
        return self.map[layer][pos.x][pos.y]

    def tile_properties(self, layer: str, pos: Vector2):
        return self.tile(layer, pos).properties

    def get_tiles_by_attr(self, attribute, layer) -> list:
        tiles = [tile for tile in iter(self.groups[layer]) if tile.has(attribute)]
        return tiles

    def get_tile_attrs(self, tile, layer) -> dict:
        return self.maps[layer][tile].properties

    def set_tile(self, tile_pos, layer: str, tile_id=0):
        # TODO
        pass

    def world_to_map(self, world_pos: Vector2) -> Vector2:
        return Vector2(
            floor(world_pos.x / self.tmx_data.tilewidth),
            floor(world_pos.y / self.tmx_data.tileheight),
        )

    def map_to_world(self, x, y) -> Vector2:
        return Vector2(
            x * self.tmx_data.tilewidth,
            y * self.tmx_data.tileheight,
        )

    def map_to_worldv(self, map_pos: Vector2) -> Vector2:
        return Vector2(
            map_pos.x * self.tmx_data.tilewidth,
            map_pos.y * self.tmx_data.tileheight,
        )


class WorldTilemap(Tilemap):
    """Game-specific Tilemap. Holds layers spectific to this game, and game-specific convenience functions."""

    def __init__(self, tmx_file):
        groups = ["ground", "plants and graves"]
        super().__init__(tmx_file, groups)

    def get_tilled_soil(self):
        return self.get_tiles_by_attr("Plantable", "ground")
