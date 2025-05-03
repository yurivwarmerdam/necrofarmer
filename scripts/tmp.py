import pygame as pg
from pytmx.util_pygame import load_pygame

pg.init()


pg.display.set_mode((1280, 960))
pg.Surface((640, 480))

txmdata=load_pygame("art/tmx/field.tmx")

# print(dir(my_tmx.tilesets[0]))
print(txmdata.tile_properties) # all tile properties
print(txmdata.get_tile_properties(14,8,1)) # get an indivitual tiles' properties, if any.