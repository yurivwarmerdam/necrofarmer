from pygame.sprite import Group
from scripts.tilemap import Tilemap, Tile
from pygame import Vector2, Surface
import json


class BigTile:
    def __init__(
        self,
        pos,
        image: Surface,
        tile_properties: dict,
        # still need the following, prolly
        # tile_size: Vector2,
        # tile_origin: Vector2,
        # *groups,
    ):
        """
        Currently only suports isometric tiles.
        Should also be compatible with orthogonal tiles with comparatively little effort.
        Args:
            pos: position of tile
            image: image to be sliced into subtiles
            tile_properties: will be passed to all subtiles
            tiles: positions of subtiles
            tile_size: size of a single tile
            tile_origin: vector pointing to the bottomleft corner of the tile with idx 0,0
        """
        self.pos = pos
        self.sprites = {}
        tile_idxs = self.bigtile_prop_to_vectors(tile_properties["bigtile"])
        left_idxs = self.find_left_overdraw_tile_idxs(tile_idxs)
        right_idxs = self.find_right_overdraw_tile_idxs(tile_idxs)
        

        print(left_idxs, right_idxs)

        for tile in tile_idxs:
            ## naive tile height
            tile_image = Surface((tile_size.x, image.get_rect().height))
            pass

        self.tiles = tile_idxs

    def bigtile_prop_to_vectors(self, property):
        return [Vector2(*p) for p in json.loads(property)]

    def find_left_overdraw_tile_idxs(self, tiles: list[Vector2]):
        left_tilesum = min([tile.x - tile.y for tile in tiles])
        return [tile for tile in tiles if tile.x - tile.y == left_tilesum]

    def find_right_overdraw_tile_idxs(self, tiles: list[Vector2]):
        right_tilesum = max([tile.x - tile.y for tile in tiles])
        return [tile for tile in tiles if tile.x - tile.y == right_tilesum]


class EntityTilemap(Tilemap):
    def __init__(
        self,
        tmx_file,
    ):
        super().__init__(tmx_file)
        for layer in self.layers:
            bigtiles = self.get_tile_idxs_by_property("bigtile", layer)

            for tile_pos in bigtiles:
                # print(self.get_tile(layer, tile_pos))
                tile: Tile = self.get_tile(layer, tile_pos)
                self.kill_tile(layer, tile_pos)
                bigtile = BigTile(tile_pos, tile.image, tile.properties)
                #something like:
                # sub_poses=[Vector2(*p) for p in json.loads(tile.properties["bigtile"])]
                # for sub_pos in sub_poses:
                #   self.map_to_world(sub_pos+tile_pos)

        # Ok, so I can make tiles.
        # Now, how do I want to address it as more of an entity?
        # expected access patterns:
        # - click (+find its corresponding UI elements)
        # - feed into UI element
        # - find back the entity from some child process 
        #       (unit creation, replacement by upgrade, perhaps more)