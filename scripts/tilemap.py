import pygame as pg
from pygame.sprite import Sprite, Group
from pytmx.util_pygame import load_pygame


class Tile(Sprite):
    def __init__(self, pos, surf, tile_properties: dict, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.properties: dict = tile_properties if tile_properties else {}

    def has(self, attribute):
        return attribute in self.properties


class Tilemap:
    """Generic Tilemap. Holds several layers of Sprite Groups."""

    def __init__(self, tmx_file, groups):
        self.tmx_data = load_pygame(tmx_file)
        self.layers = {}

        for group in groups:
            self.layers[group] = Group()
        for layer in self.tmx_data.visible_layers:
            if layer.name in groups and hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                    gid = layer.data[y][x]  # Warning: y x != x y
                    tile_properties = self.tmx_data.get_tile_properties_by_gid(gid)
                    Tile(pos, surf, tile_properties, self.layers[layer.name])

    def get_layer(self, layer):
        return self.layers[layer]

    def get_neigbors(pos, distance=1):
        result = []
        for x in range(-distance, distance):
            for y in range(-distance, distance):
                if (x, y) == pos:
                    continue
                result.append((x, y))
        return result

    def set_tile(self, tile_pos, layer: str, tile_id=0):
        # TODO
        pass

    def get_tiles_by_attr(self, attribute, layer) -> list:
        tiles = [tile for tile in iter(self.layers[layer]) if tile.has(attribute)]
        return tiles

    def get_tile_attrs(self, tile, layer) -> dict:
        return self.layers[layer][tile].properties


class world_tilemap(Tilemap):
    """Game-specific Tilemap. Holds layers spectific to this game, and game-specific convenience functions."""

    def __init__(self, tmx_file):
        groups = ["ground", "plants and graves"]
        super().__init__(tmx_file, groups)

    def get_tilled_soil(self):
        return self.get_tiles_by_attr("Plantable", "ground")
