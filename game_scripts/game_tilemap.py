from game_scripts.entity_tilemap import EntityTilemap


class GameTilemap(EntityTilemap):
    pass


_instance = None


# TODO: how to deal with re-instantiating tilemap on load, level change, map expansion, whatever.
def get_tilemap(tmx_path: str | None = None) -> GameTilemap:
    global _instance
    if _instance is None and tmx_path is None:
        raise Exception("Tilemap server not yet initiated with a map.")
    elif _instance is None:
        _instance = GameTilemap(tmx_path)
    return _instance
