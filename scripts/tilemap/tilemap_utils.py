from math import floor

from pygame import Vector2


def map_to_world(x, y, tilewidth, tileheight, isometric=False) -> Vector2:
    if isometric:
        return Vector2(
            tilewidth / 2 * (x - y),
            tileheight / 2 * (x + y),
        )
    else:
        return Vector2(
            x * tilewidth,
            y * tileheight,
        )


def map_to_worldv(map_pos: Vector2, tile_size: Vector2, isometric=False):
    return map_to_world(map_pos.x, map_pos.y, tile_size.x, tile_size.y, isometric)


def world_to_map(world_x, world_y, tilewidth, tileheight, isometric=False):
    if isometric:
        half_w = tilewidth / 2
        half_h = tileheight / 2
        x = (((world_x / half_w) + (world_y / half_h)) / 2) + 0.5
        y = (((world_y / half_h) - (world_x / half_w)) / 2) + 0.5

        return Vector2(floor(x), floor(y))
    else:
        return Vector2(
            floor(world_x / tilewidth),
            floor(world_y / tileheight),
        )


def world_to_mapv(world_pos: Vector2, tile_size: Vector2, isometric=False):
    return world_to_map(world_pos.x, world_pos.y, tile_size.x, tile_size.y, isometric)
