from scripts.tilemap import Tilemap
from pygame.sprite import Group


class WorldTilemap(Tilemap):
    """Game-specific Tilemap. Holds layers spectific to this game, and game-specific convenience functions."""

    def __init__(self, tmx_file, render_layers: dict[str, Group]):
        groups = {
            "ground": render_layers["ground"],
            "plants and graves": render_layers["active"],
        }
        super().__init__(tmx_file, groups)

    def get_tilled_soil(self):
        return self.get_tiles_by_attr("Plantable", "ground")
