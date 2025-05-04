import pygame as pg
from pytmx.util_pygame import load_pygame

pg.init()


pg.display.set_mode((1280, 960))
pg.Surface((640, 480))

txmdata = load_pygame("art/tmx/field.tmx")

# print(dir(my_tmx.tilesets[0]))
print(txmdata.tile_properties)  # all tile properties
# get an indivitual tiles' properties, if any.
print(txmdata.get_tile_properties(9, 8, 0))
print(txmdata.get_tile_properties(14, 8, 1))
print(txmdata.layers)

for layer in txmdata.layers:
    print(dir(layer))
    print("-giddy?-")
    print(layer.data[8][8])
    print(layer.data[8][14])
    print("/-giddy?-")
    print(layer.id)

for i in range(len(txmdata.layers)):
    layer=txmdata.layers[i]
    print("Layer nonsense:", i, layer.id)
    # print(dir(layer))
