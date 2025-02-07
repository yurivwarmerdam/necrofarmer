import pygame as pg
from pytmx.util_pygame import load_pygame


screen = pg.display.set_mode((1280, 960))
display = pg.Surface((640, 480))

# self.tmx_data = load_pygame("art/tmx/field.tmx")
# tile_group = pg.sprite.Group()


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class Tilemap():
    def __init__(self,tmx_file,groups):
        self.tmx_data=load_pygame(tmx_file)
        self.layers={}
        for group in groups:
            self.layers[group] = pg.sprite.Group()
        for layer in self.tmx_data.visible_layers:
            if layer.name in groups and hasattr(layer,"data"):
                for x, y, surf in layer.tiles():
                    pos = (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                    Tile(pos, surf, self.layers[layer.name])


    def get_layer(self,layer):
        return self.layers[layer]
