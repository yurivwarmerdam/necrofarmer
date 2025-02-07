import pygame as pg
# from pygame import Surface, sprite
from pytmx.util_pygame import load_pygame


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
    
    def get_neigbors(pos,distance=1):
        result=[]
        for x in range(-distance,distance):
            for y in range(-distance,distance):
                if (x,y) == pos:
                    continue
                result.append((x,y))
        return result


    def set_tile(self, tile_pos,layer,tile_id=0):
        if tile_id == 0:
            self.layers[layer]
        pass

    # def __init__(self, game, tiles, tile_size=(16, 16), map_size=(12, 10, 1)):
    #     self.game = game
    #     self.tile_size = tile_size
    #     self.tiles = tiles
    #     self.tiles.append(None)

    #     # access as x,y,z! (x right, y down, x stacked)
    #     # TODO: Use np here
    #     self.tilemap = [
    #         [[-1 for _ in range(map_size[2])] for _ in range(map_size[1])]
    #         for _ in range(map_size[0])
    #     ]

    # def local_to_map(self, local):
    #     return (local[0] // self.tile_size[0], local[1] // self.tile_size[1])

    # def map_to_local(self, map_loc):
    #     return (map_loc[0] * self.tile_size[0], map_loc[0] * self.tile_size[0])

    # # TODO: THis might be better characterized as for col in array (which is rows) etc.
    # def render(self, surface: Surface):
    #     for x, rows in enumerate(self.tilemap):
    #         x_surface = x * self.tile_size[0]
    #         for y, cols in enumerate(rows):
    #             y_surface = y * self.tile_size[1]
    #             for z in cols:
    #                 if z != -1:
    #                     surface.blit(self.tiles[z], (x_surface, y_surface))

    # def set_cell(self, x, y, z=0, tile_idx=0):
    #     self.tilemap[x][y][z] = tile_idx
    #     print(self.tilemap)
