from game_scripts.entity_tilemap import EntityTilemap
from pygame.math import Vector2


class GameTilemap(EntityTilemap):
    def get_tree_idxs(self):
        return self.get_tile_idxs_by_property("wood", "active")

    def get_closest_local_tree_idx(self, to: Vector2):
        trees = self.get_tree_idxs()
        return min(trees, key=lambda p: (p[0] - to.x) ** 2 + (p[1] - to.y) ** 2)


_instance = None


# TODO: how to deal with re-instantiating tilemap on load, level change, map expansion, whatever.
def get_tilemap(tmx_path: str | None = None) -> GameTilemap:
    global _instance
    if _instance is None and tmx_path is None:
        raise Exception("Tilemap server not yet initiated with a map.")
    elif _instance is None:
        _instance = GameTilemap(tmx_path)
    return _instance
