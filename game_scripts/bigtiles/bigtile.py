import json

from pygame import Vector2

from scripts.tilemap import Tile, TileData
from scripts.group_server import get_group_server


class BigTile(Tile):
    def __init__(self, tiledata: TileData):
        """
        Currently only suports isometric tiles.
        Should also be compatible with orthogonal tiles with comparatively little effort.
        """

        groups = [get_group_server().update]
        if mask := tiledata.properties.get("collision_mask"):
            groups += get_group_server().get_collide_groups_by_mask(mask)
        super().__init__(tiledata, *groups)
        self.tiles: list[Vector2] = bigtile_prop_to_vectors(
            tiledata.properties["bigtile"]
        )


def bigtile_prop_to_vectors(property) -> list[Vector2]:
    return [Vector2(*p) for p in json.loads(property)]
