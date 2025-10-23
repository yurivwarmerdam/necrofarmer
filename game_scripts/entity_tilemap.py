from pygame.sprite import Group, Sprite
from scripts.tilemap import Tilemap, Tile
from pygame import Vector2, Surface
import json
from math import floor


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
            image: image to be sliced into subtiles
            properties: tile properties
            groups: groups this sprite will belong to
            anchor: Sprite anchor
            offset: vector pointing from anchor intended origin of the tile.
            tiles: map_idxs of all subtiles within this bigtile
        """
        super().__init__(pos, image, properties, *groups, anchor=anchor, offset=offset)
        self.tiles = tiles
        print(self.pos, self.tiles)

    def bigtile_prop_to_vectors(self, property):
        return [Vector2(*p) for p in json.loads(property)]

class EntityTilemap(Tilemap):
    def __init__(
            self,
            tmx_file,
    ):
        super().__init__(tmx_file)
        self.bigtiles: dict[Vector2, BigTile] = {}
        for layer in self.layers:
            bigtile_map_idxs = self.get_tile_idxs_by_property("bigtile", layer)

            for origin_idx in bigtile_map_idxs:
                tile: Tile = self.get_tilev(layer, origin_idx)
                self.kill_tile(layer, origin_idx)
                sub_idxs = [Vector2(*p) for p in json.loads(tile.properties["bigtile"])]
                sub_idxs = [idx + origin_idx for idx in sub_idxs]
                if not self.is_valid_placement_idxs(sub_idxs, layer):
                    raise Exception(
                        "invalid BigTile Placement in EntityTilemap init! Aborting."
                    )
                new_tile = BigTile(
                    tile.pos,
                    tile.image,
                    tile.properties,
                    tile.groups(),
                    anchor=tile.anchor,
                    offset=tile.offset,
                    tiles=sub_idxs,
                )
                self.bigtiles[new_tile] = sub_idxs
                self.set_tile(new_tile, layer, origin_idx)

    def set_tile(self, tile: Tile, layer: str, map_pos: Vector2):
        super().set_tile(tile, layer, map_pos)
        if isinstance(tile, BigTile):
            for subtile in tile.tiles:
                self.map[layer][floor(subtile.x)][floor(subtile.y)] = tile

    def is_valid_placement_idxs(self, idxs: list[Vector2], layer):
        return all(self.get_tilev(layer, x) is None for x in idxs)
