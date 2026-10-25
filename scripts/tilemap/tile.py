from math import floor

from pygame import Vector2
from pytmx.map import TiledLayer, TiledMap
from pytmx.util_pygame import load_pygame

from scripts.custom_sprites import NodeSprite
from scripts.group_server import get_group_server
from scripts.tilemap.tiledata import TileData


class Tile(NodeSprite):
    def __init__(self, Tiledata: TileData, *groups):
        if mask := Tiledata.get_property("collision_mask"):
            collide_groups = get_group_server().get_collide_groups_by_mask(mask)
            groups = groups + tuple(collide_groups)
        super().__init__(
            Tiledata.surf, Tiledata.world_pos, Tiledata.anchor, Tiledata.offset, *groups
        )
        self.properties = Tiledata.properties

    @property
    def collision_mask(self) -> int:
        return self.properties.get("collision_mask", 0)

    def has(self, attribute):
        return attribute in self.properties


class TileDataLayers:
    # TODO: maybe implement __getItem__?
    def __init__(
        self,
        tmx_data: TiledMap | str,
        tile_types: dict[str, type[Tile]] = {},
    ):
        """
        container object for layer of TileData.
        params:
        tmx_data: Preloaded tmx data. If a string is supplied it is extracted, instead.
        tile_types: optional dict of custyom tile types. Any types not recognized will default to specifying Tile.
        """
        if isinstance(tmx_data, str):
            tmx_data = load_pygame(tmx_data)
        self.tmx_data = tmx_data
        self.tile_types = tile_types
        self.tile_size = Vector2(tmx_data.tilewidth, tmx_data.tileheight)
        self.isometric = self.tmx_data.orientation == "isometric"
        self.named_tiles = {}

        self.layers: dict[str, dict[Vector2, TileData]] = {}

        # tmx_data = load_pygame(tmx_file)
        for source_layer in tmx_data.visible_layers:
            if hasattr(source_layer, "data"):
                self.layers[source_layer.name] = self.make_layerdata(source_layer)

    def make_layerdata(self, source_layer: TiledLayer) -> dict[Vector2, TileData]:
        layer = {}
        for x, y, surf in source_layer.tiles():
            tile = self.make_tiledata(source_layer, x, y, surf)
            layer[(x, y)] = tile
        return layer

    def make_tiledata(self, tmx_layer, x, y, surf):
        pytmx_gid = tmx_layer.data[y][x]  # Warning: y x != x y
        tileset = self.tmx_data.get_tileset_from_gid(pytmx_gid)
        offset = -(
            Vector2(tileset.offset)
            + (-floor(self.tmx_data.tilewidth / 2), floor(self.tmx_data.tileheight / 2))
        )
        properties: dict = self.tmx_data.get_tile_properties_by_gid(pytmx_gid) or {}
        tile_type = self.tile_types.get(properties.get("name", ""), Tile)
        new_data = TileData(
            tile_type=tile_type,
            map_pos=Vector2(x, y),
            tile_size=self.tile_size,
            properties=properties,
            surf=surf,
            offset=offset,
            isometric=self.isometric,
        )
        if "name" in properties.keys():
            if properties["name"] not in self.named_tiles:
                self.named_tiles[properties["name"]] = new_data.move(Vector2(0, 0))
        return new_data