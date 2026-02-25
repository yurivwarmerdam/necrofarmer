import pygame as pg
from pygame import Rect, Surface
from pygame.math import Vector2

# from typing import List


def load_image(path) -> Surface:
    image = pg.image.load(path).convert()
    image.set_colorkey((0, 0, 0, 0))
    return image


# no support for padding
def sheet_to_sprites(spritesheet: Surface, size: Vector2) -> dict:
    """
    Slice spritesheet into subsurfaces of size.
    Returns a dict of surfaces, accesssed by (col,row).

    :param spritesheet: surface to be sliced
    :type spritesheet: Surface
    :param size: Description
    :type size: Vector2
    :return: Description
    :rtype: dict[Any, Any]
    """
    cols = int(spritesheet.get_size()[0] / size.x)
    rows = int(spritesheet.get_size()[1] / size.y)
    sprites = {}
    for col in range(cols):
        for row in range(rows):
            rect = pg.Rect(col * size.x, row * size.y, size.x, size.y)
            sprite = Surface(size).convert()
            sprite.set_colorkey((0, 0, 0, 0))
            sprite.blit(spritesheet, (0, 0), rect)
            sprites[(col, row)] = sprite
    return sprites


def sheet_to_sprite(spritesheet: Surface, subsurf_rect: Rect) -> Surface:
    """
    take a surface, and return a subsurface located at subsurf_rect.

    :param spritesheet: surface to be accessed
    :type spritesheet: Surface
    :param subsurf_rect: rectangle to locate at
    :type subsurf_rect: Rect
    """
    sprite = Surface(subsurf_rect.size).convert()
    sprite.blit(spritesheet, area=subsurf_rect)
    sprite.set_colorkey((0, 0, 0, 0))
    return sprite


# no support for padding
# That's this FOR, then?
def sheet_to_sprites_with_pad(sheet: Surface, tile_size: Vector2, pad=(0, 0)) -> dict:
    sprites = []
    remaining_x = sheet.get_size()[0]

    while remaining_x >= tile_size[0]:
        pass

    cols = int(sheet.get_size()[0] / tile_size.x)
    rows = int(sheet.get_size()[1] / tile_size.y)
    sprites = {}
    for col in range(cols):
        for row in range(rows):
            rect = pg.Rect(
                col * tile_size.x, row * tile_size.y, tile_size.x, tile_size.y
            )
            sprite = Surface(tile_size).convert()
            sprite.blit(sheet, (0, 0), rect)
            sprites[(col, row)] = sprite
    return sprites
