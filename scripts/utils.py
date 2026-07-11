import pygame as pg
from pygame import Rect, Surface
from pygame.mask import from_surface
from pygame.math import Vector2
from pygame.sprite import Sprite


# from typing import List


# TODO: keep references to surfaces that were previously loaded.
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


def sheet_to_sprite(spritesheet: Surface | str, subsurf_rect: Rect) -> Surface:
    """
    take a surface, and return a subsurface located at subsurf_rect.

    Parameters:
        spritesheet: surface to be accessed. If a string is supplied, it is first loaded as a file.
        subsurf_rect: rectangle to locate at
    Returns:
        a single subsurface
    """
    if isinstance(spritesheet, str):
        spritesheet = load_image(spritesheet)
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


def pointcollide_mask(point: tuple[int, int], sprite: Sprite) -> bool:
    """
    collision detection between a point and a sprite, using masks.

    pygame.sprite.collide_mask(point, sprite): bool

    Tests for collision between a point and a sprite by testing if the sprites' bitmask
    is occupied at the point. If the sprite has a "mask" attribute, that is used as the mask;
    otherwise, a mask is created from the sprite image. Intended to be passed
    as a collided callback function to pointcollide. Sprites must
    have a "rect" and an optional "mask" attribute.
    """
    xoffset = point[0] - sprite.rect[0]
    yoffset = point[1] - sprite.rect[1]
    try:
        mask = sprite.mask
    except AttributeError:
        mask = from_surface(sprite.image)

    if (
        xoffset < 0
        or xoffset >= mask.get_size()[0]
        or yoffset < 0
        or yoffset >= mask.get_size()[1]
    ):
        return False
    return bool(mask.get_at((xoffset, yoffset)))


def pointcollide(point, group, collide_callback=None):
    """Kind of extra for now. However, it mostly follows the pattern of *collide functions in official pygame."""
    default_callback = pointcollide_mask

    if collide_callback is not None:
        return [sprite for sprite in group if collide_callback(point, sprite)]

    return [sprite for sprite in group if default_callback(point, sprite)]

    pass
