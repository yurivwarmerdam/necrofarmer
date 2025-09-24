from pygame.sprite import Group, Sprite
from scripts.tilemap import Tilemap, Tile
from pygame import Vector2, Surface
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
            image: image to be sliced into subtiles
            properties: tile properties
            groups: groups this sprite will belong to
            anchor: Sprite anchor
            offset: vector pointing from anchor intended origin of the tile.
            tiles: map_idxs of all subtiles within this bigtile
        """
        print("in bigtile:", groups)
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
        # bigtiles:
        # bigtiles[Vector2(x,y)]=entity
        self.bigtiles: dict[Vector2, BigTile] = {}
        for layer in self.layers:
            bigtile_map_idxs = self.get_tile_idxs_by_property("bigtile", layer)

            # TODO: naming is hard
            for big_idx in bigtile_map_idxs:
                tile: Tile = self.get_tilev(layer, big_idx)
                print(tile.groups())
                # 1/0
                self.kill_tile(layer, big_idx)
                sub_idxs = [Vector2(*p) for p in json.loads(tile.properties["bigtile"])]
                sub_idxs = [idx + big_idx for idx in sub_idxs]
                if not self.is_valid_placement_idxs(sub_idxs, layer):
                    raise Exception(
                        "invalid BigTile Placement in EntityTilemap init! Aborting."
                    )
                print(sub_idxs)
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
                for sub_idx in sub_idxs:
                    self.set_tile(new_tile, layer, sub_idx)

    def is_valid_placement_idxs(self, idxs: list[Vector2], layer):
        return all(self.get_tilev(layer, x) is None for x in idxs)

    # Ok, so I can make tiles.
    # Now, how do I want to address it as more of an entity?
    # expected access patterns:
    # - click (+find its corresponding UI elements)
    # - feed into UI element
    # - find back the entity from some child process
    #       (unit creation, replacement by upgrade, perhaps more)
    # since Groups have a 2-way dependence (tiles know theeir groups, and groups know their tiles)
    # So it's acceptible to do a similar thing for this type of tilemap
    # possibly using BigTile as an n:m decoupling thing.

    # First, let's look at the way this works for Groups and Sprites
    # Ok, done. Both just have references to each other. Fine.
