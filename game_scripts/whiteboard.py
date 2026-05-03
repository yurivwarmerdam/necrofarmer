from scripts.tilemap import TileDataLayers, TileData
from game_scripts.bigtiles import bigtiles

# statics
bigtile_entities = {
    "sawmill": bigtiles.Sawmill,
    "thopter_factory_2": bigtiles.ThopterFactory,
}
button_ids = {
    "#thopter_button": "0,0,46,38",
    "#tardigrade_button": "138,0,46,38",
    "#sawmill_button": "230,0,46,38",
    "#thopter_factory_2_button": "184,76,46,38",
    "#thopter_factory_button": "138,76,46,38",
}


class Whiteboard:
    """
    Global whiteboard. Has some predefined and preloaded stuff.
    Can also freely be written to for unnamed things
    so, like:
    class other_script():
      Whiteboard.weird_var="value"
      use_variable(whiteboard.weird_var)
    """

    # Ohgod, how could I possibly avoid circular import warnings!?

    def __init__(self) -> None:
        self.tile_entities: dict[str, TileData] = self.parse_tiledata()
        print(len(self.tile_entities))

    def parse_tiledata(self):
        file_data = TileDataLayers(
            "tilemaps/tile_entities.tmx", bigtile_entities
        ).layers["tile_entities"]
        tile_entities: dict[str, TileData] = {}

        for key in bigtile_entities:
            for idx in file_data:
                if file_data[idx].tile_type == bigtile_entities[key]:
                    tile_entities[key] = file_data[idx]
        return tile_entities


_instance: Whiteboard | None = None


def get_Whiteboard() -> Whiteboard:
    global _instance
    if _instance is None:
        _instance = Whiteboard()
    return _instance
