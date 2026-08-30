from typing import override

from pygame import Vector2

from game_scripts import whiteboard
from game_scripts.bigtiles.bigtile import BigTile
from scripts.tilemap import Tile, Tilemap, TileData


# I want to become a more generic class.
# TODO: Work out what I want to make more/less generic.
class EntityTilemap(Tilemap):
    def __init__(self, tmx_path):
        super().__init__(tmx_path, whiteboard.bigtile_entities)
        self.bigtiles: dict[str, dict[tuple[int, int], BigTile]] = {}
        for layer in self.layers:
            self.bigtiles[layer] = {}
            for idx in self.get_tile_idxs_by_property("bigtile", layer):
                self.bigtiles[layer][idx] = self.get_tile(layer, *idx)

    @override
    def set_tile_in_map(self, tile: Tile, layer: str, map_pos: Vector2) -> bool:
        if isinstance(tile, BigTile):
            tiles_positioned = [subtile + map_pos for subtile in tile.tiles]
            if not self.is_valid_placement_idxs(tiles_positioned, layer):
                return False
            for subtile in tile.tiles:
                super().set_tile_in_map(tile, layer, subtile + map_pos)
            return True
        else:
            return super().set_tile_in_map(tile, layer, map_pos)

    # This should probably also be an override of some default behavior.
    def spawn_tile(self, tile_data: TileData, layer_name: str):
        new_tile = tile_data.tile_type(tile_data)
        if not self.set_tile_in_map(new_tile, layer_name, tile_data.map_pos):
            print("erroneous tile placement! This an unwanted state? Killing the newborn.")
            new_tile.kill()



    def is_valid_placement_idxs(self, idxs: list[Vector2], layer: str):
        """
        list-based verison of is_valid_placement.
        """
        return all(self.is_valid_placement(x, layer) for x in idxs)
