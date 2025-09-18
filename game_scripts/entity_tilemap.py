from pygame.sprite import Group
from scripts.tilemap import Tilemap, Tile
from pygame import Vector2, Surface


class BigTile:
    def __init__(
        self,
        pos,
        image: Surface,
        tile_properties: dict,
        tile_idxs: list[Vector2],
        tile_size: Vector2,
        tile_origin: Vector2,
        *groups,
    ):
        """
        Currently only suports isometric tiles.
        Should also be compatible with orthogonal tiles with comparatively little effort.
        Args:
            pos: position of tile
            image: image to be sliced into subtiles
            tile_properties: will be passed to all subtiles
            tiles: positions of subtiles
            tile_size: size of a single tilear
            tile_origin: vector pointing to the bottomleft corner of the tile with idx 0,0
        """
        self.pos = pos
        self.sprites = {}
        left_tile_idx = find_left_overdraw_tile_idx(tile_idxs)
        right_tile_idx = find_right_overdraw_tile_idx(tile_idxs)

        for tile in tile_idxs:
            ## naive tile height
            tile_image = Surface((tile_size.x, image.get_rect().height))
            pass

        left_overdraw = 0
        right_overdraw = 0

        self.tiles = tile_idxs

        def find_left_overdraw_tile_idx(tiles: list[Vector2]):
            left_tile = tiles[0]
            for tile in tiles:
                # is tile more left
                if tile.x - tile.y <= left_tile.x - left_tile.y:
                    # is tile further down
                    if tile.x + tile.y > left_tile.x + left_tile.y:
                        left_tile = tile
            return left_tile

        def find_right_overdraw_tile_idx(tiles: list[Vector2]):
            right_tile = tiles[0]
            for tile in tiles:
                # is tile more right
                if tile.x - tile.y >= right_tile.x - right_tile.y:
                    # is tile further down
                    if tile.x + tile.y > right_tile.x + right_tile.y:
                        right_tile = tile
            return right_tile


class EntityTilemap(Tilemap):
    def __init__(
        self,
        tmx_file,
        group_mappings: dict[str, Group],
        # tile_entity_mapping: dict[str, type],
    ):
        super().__init__(tmx_file, group_mappings)
        for layer in self.layers:
            bigtiles = self.get_tile_idxs_by_property("bigtile", layer)
            print(bigtiles)
            for tile in bigtiles:
                print(self.tile(layer,tile))
