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

    def bigtile_prop_to_vectors(self, property):
        return [Vector2(*p) for p in json.loads(property)]

    def find_left_overdraw_tile_idxs(self, tiles: list[Vector2]):
        """Deprecated"""
        left_tilesum = min([tile.x - tile.y for tile in tiles])
        return [tile for tile in tiles if tile.x - tile.y == left_tilesum]

    def find_right_overdraw_tile_idxs(self, tiles: list[Vector2]):
        """Deprecated"""
        right_tilesum = max([tile.x - tile.y for tile in tiles])
        return [tile for tile in tiles if tile.x - tile.y == right_tilesum]


class EntityTilemap(Tilemap):
    def __init__(
        self,
        tmx_file,
    ):
        super().__init__(tmx_file)
        self.bigtiles: dict[Vector2, BigTile] = {}
        for layer in self.layers:
            bigtile_map_idxs = self.get_tile_idxs_by_property("bigtile", layer)

            for big_idx in bigtile_map_idxs:
                tile: Tile = self.get_tilev(layer, big_idx)
                self.kill_tile(layer, big_idx)
                sub_idxs = [Vector2(*p) for p in json.loads(tile.properties["bigtile"])]
                sub_idxs = [idx + big_idx for idx in sub_idxs]
                if not self.is_valid_placement_idxs(sub_idxs, layer):
                    raise Exception(
                        "invalid BigTile Placement in EntityTilemap init! Aborting."
                    )
                new_tile = BigTile(
                    Vector2(0, 0),
                    tile.image,
                    tile.properties,
                    tile.groups(),
                    anchor=tile.anchor,
                    offset=tile.offset,
                    tiles=sub_idxs,
                )
                self.bigtiles[new_tile] = sub_idxs
                self.set_tile(new_tile, layer, big_idx)

    def set_tile(self, tile: Tile, layer: str, map_pos: Vector2):
        super().set_tile(tile, layer, map_pos)
        if isinstance(tile, BigTile):
            for subtile in tile.tiles:
                self.map[layer][floor(map_pos.x)][floor(map_pos.y)] = tile

    def is_valid_placement_idxs(self, idxs: list[Vector2], layer):
        return all(self.get_tilev(layer, x) is None for x in idxs)
