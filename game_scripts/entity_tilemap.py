import json
from math import floor

from pygame import Vector2

from game_scripts.bigtiles.bigtile import BigTile
from game_scripts.bigtiles import bigtiles
from scripts.tilemap import Tile, Tilemap

# TODO: this wants to be in some .conf or json file.
bigtile_entities = {
    "sawmill": bigtiles.Sawmill,
    "thopter_factory_2": bigtiles.ThopterFactory,
}


class EntityTilemap(Tilemap):
    def __init__(self, tmx_path):
        super().__init__(tmx_path, bigtile_entities)
        self.bigtiles: dict[str, dict[tuple[int, int], BigTile]] = {}
        for layer in self.layers:
            self.bigtiles[layer] = {}
            for idx in self.get_tile_idxs_by_property("bigtile", layer):
                self.bigtiles[layer][idx] = self.get_tile(layer, *idx)

    def set_tile(self, tile: Tile, layer: str, map_pos: Vector2):
        if isinstance(tile, BigTile):
            if not self.is_valid_placement_idxs(tile.tiles, layer):
                raise Exception(
                    "invalid BigTile Placement in EntityTilemap init! Aborting."
                )
            for subtile in tile.tiles:
                super().set_tile(tile, layer, subtile + map_pos)
        else:
            super().set_tile(tile, layer, map_pos)

    def is_valid_placement_idxs(self, idxs: list[Vector2], layer):
        return all(self.get_tilev(layer, x) is None for x in idxs)


_instance = None


# TODO: how to deal with re-instantiating tilemap on load, level change, map expansion, whatever.
def get_tilemap(tmx_path: str | None = None) -> EntityTilemap:
    global _instance
    if _instance is None and tmx_path is None:
        raise Exception("Tilemap server not yet initiated with a map.")
    elif _instance is None:
        _instance = EntityTilemap(tmx_path)
    return _instance
