from typing import override

from pygame import Vector2

from game_scripts import whiteboard
from game_scripts.bigtiles.bigtile import BigTile, bigtile_prop_to_vectors
from scripts.tilemap import Tile, Tilemap, TileData


# I want to become a more generic class.
# TODO: Work out what I want to make more/less generic.
class EntityTilemap(Tilemap):
    def __init__(self, tmx_path):
        super().__init__(tmx_path, whiteboard.bigtile_entities)
        self.bigtiles: dict[str, dict[tuple[int, int], BigTile]] = {}
        # for layer in self.layers:
        #     self.bigtiles[layer] = {}
        #     for idx in self.get_tile_idxs_by_property("bigtile", layer):
        #         self.bigtiles[layer][idx] = self.get_tile(layer, *idx)

    @override
    def set_tile_in_map(self, tile: Tile, layer: str, map_pos: Vector2) -> bool:
        if isinstance(tile, BigTile):
            for subtile in tile.tiles:
                super().set_tile_in_map(tile, layer, subtile + map_pos)
            return True
        else:
            return super().set_tile_in_map(tile, layer, map_pos)

    @override
    def can_spawn_tile(self, tile_data: TileData, layer: str):
        bigtile = tile_data.get_property("bigtile")
        if bigtile:
            vectors = bigtile_prop_to_vectors(bigtile)
            vectors = [vector + tile_data.map_pos for vector in vectors]
            result = [
                super().can_spawn_tile(tile_data.move(vector), layer)
                for vector in vectors
            ]
            return all(result)
        else:
            return super().can_spawn_tile(tile_data, layer)
