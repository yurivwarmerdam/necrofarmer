from game_scripts import bigtiles
from scripts.tilemap import TileData, TileDataLayers

# statics
bigtile_entities = {
    "_sawmill": bigtiles._Sawmill,
    "sawmill": bigtiles.Sawmill,
    "thopter_factory_2": bigtiles.ThopterFactory,
}
button_ids = {
    "#thopter_button": "0,0,46,38",
    "#tardigrade_button": "138,0,46,38",
    "#sawmill_button": "230,0,46,38",
    "#_sawmill_button": "276,0,46,38",
    "#thopter_factory_2_button": "184,76,46,38",
    "#thopter_factory_button": "138,76,46,38",
    "#haul_logs_button": "46,114,46,38",
    "#thopter_cancel_button": "92,114,46,38",
    "#cancel_button": "0,76,46,38",
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

    def __init__(self) -> None:
        print("not actually implemented! So far everything's static here, yo.")


_instance: Whiteboard | None = None


def get_Whiteboard() -> Whiteboard:
    global _instance
    if _instance is None:
        _instance = Whiteboard()
    return _instance
