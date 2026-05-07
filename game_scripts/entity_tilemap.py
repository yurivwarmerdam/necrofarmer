from pygame import Vector2
from game_scripts import whiteboard

from game_scripts.bigtiles.bigtile import BigTile

from scripts.tilemap import Tile, Tilemap


class EntityTilemap(Tilemap):
    def __init__(self, tmx_path):
        super().__init__(tmx_path, whiteboard.bigtile_entities)
        self.bigtiles: dict[str, dict[tuple[int, int], BigTile]] = {}
        for layer in self.layers:
            self.bigtiles[layer] = {}
            for idx in self.get_tile_idxs_by_property("bigtile", layer):
                self.bigtiles[layer][idx] = self.get_tile(layer, *idx)

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

    def is_valid_placement_idxs(self, idxs: list[Vector2], layer):
        # TODO: is placement actually valid? I never really proved a negative, here.
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
