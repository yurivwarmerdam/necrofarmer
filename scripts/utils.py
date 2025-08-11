import pygame as pg
from pygame import Surface, Rect
from pygame.math import Vector2
# from typing import List


def load_image(path) -> Surface:
    image = pg.image.load(path).convert()
    image.set_colorkey((0, 0, 0, 0))
    return image


# no support for padding
def sheet_to_sprites(surface: Surface, size: Vector2) -> dict:
    cols = int(surface.get_size()[0] / size.x)
    rows = int(surface.get_size()[1] / size.y)
    sprites = {}
    for col in range(cols):
        for row in range(rows):
            rect = pg.Rect(col * size.x, row * size.y, size.x, size.y)
            sprite = Surface(size).convert()
            sprite.set_colorkey((0, 0, 0, 0))
            sprite.blit(surface, (0, 0), rect)
            sprites[(col, row)] = sprite
    return sprites


def sheet_to_sprite(surface: Surface, rect: Rect):
    sprite = Surface(rect.size).convert()
    sprite.blit(surface, rect)
    sprite.set_colorkey((0, 0, 0, 0))
    return sprite


# no support for padding
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
