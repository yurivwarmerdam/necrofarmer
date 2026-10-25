# lol. Allows for weird notation
# some_tiledata.tile.type(some_tiledata)
from dataclasses import dataclass

from pygame import Vector2
from pygame.surface import Surface

from scripts.tilemap.utils import map_to_worldv


@dataclass
class TileData:
    tile_type: type
    map_pos: Vector2
    tile_size: Vector2
    properties: dict
    surf: Surface
    offset: Vector2
    isometric: bool = False
    anchor: str = "bottomleft"

    def get_property(self, prop_name):
        return self.properties.get(prop_name)

    @property
    def world_pos(self) -> Vector2:
        return map_to_worldv(self.map_pos, self.tile_size, self.isometric)

    def move(self, map_pos):
        return TileData(
            tile_type=self.tile_type,
            map_pos=map_pos,  # Note that this is the changed one.
            tile_size=self.tile_size,
            properties=self.properties,
            surf=self.surf,
            offset=self.offset,
            isometric=self.isometric,
            anchor=self.anchor,
        )

    def move_ip(self, map_pos):
        self.map_pos = map_pos