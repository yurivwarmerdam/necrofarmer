import json

from pygame import Vector2

from scripts.tilemap import Tile, TileData


class BigTile(Tile):
    def __init__(self, tiledata: TileData, *groups):
        """
        Currently only suports isometric tiles.
        Should also be compatible with orthogonal tiles with comparatively little effort.
        """
        super().__init__(tiledata, *groups)
        self.tiles: list[Vector2] = self.bigtile_prop_to_vectors(
            tiledata.properties["bigtile"]
        )

    def bigtile_prop_to_vectors(self, property) -> list[Vector2]:
        return [Vector2(*p) for p in json.loads(property)]
