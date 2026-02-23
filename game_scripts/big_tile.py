from scripts.tilemap import Tile


from pygame import Vector2


import json


class BigTile(Tile):
    def __init__(
        self,
        pos,
        image,
        properties: dict,
        *groups,
        anchor="bottomleft",
        offset=Vector2(0, 0),
        tiles: list = [Vector2(0, 0)],
    ):
        """
        Currently only suports isometric tiles.
        Should also be compatible with orthogonal tiles with comparatively little effort.
        Args:
            pos: position of tile
            image: image
            properties: tile properties
            groups: groups this sprite will belong to
            anchor: Sprite anchor
            offset: vector pointing from anchor intended origin of the tile.
            tiles: map_idxs of all subtiles within this bigtile
        """
        super().__init__(pos, image, properties, *groups, anchor=anchor, offset=offset)
        self.tiles = tiles

    def bigtile_prop_to_vectors(self, property):
        return [Vector2(*p) for p in json.loads(property)]
