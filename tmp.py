import pygame as pg
from pygame import Vector2, Surface
from pygame.sprite import Group, Sprite
import sys
from scripts.tilemap import Tilemap
from math import floor
from scripts.utils import sheet_to_sprites, load_image
from random import randint


class AnimationSequence:
    def __init__(self, sequence: list[Surface],frame_time=100) -> None:
        self.sequence = sequence
        self.reset()

    def play(self):
        pass

    def reset(self):
        self.active_sprite = 0


class AnimatedSprite(Sprite):
    def __init__(
        self,
        images: list[AnimationSequence],
        pos: Vector2,
        *groups,
    ) -> None:
        super().__init__(*groups)
        self.active_sprite = 0
        self.active_animation = next(iter(animations.items()))
        self.images = images
        self.image = images[self.active_sprite]
        self.rect = self.image.get_rect()
        self.pos = pos

    def set_image(self, image_idx):
        self.active_sprite = image_idx
        self.image = self.images[image_idx]
        pass


pg.init()

display = pg.display.set_mode((800, 400), pg.SCALED, pg.RESIZABLE)
clock = pg.time.Clock()

# tilemap
tile_layer = Group()
tilemap = Tilemap("art/tmx/tst_square_map.tmx", {"ground": tile_layer})
anim_layer = Group()

# animated sprite
images_d = sheet_to_sprites(load_image("art/tardigrade.png"), Vector2(80, 80))
print(images_d)

AnimationSequence(
    images_d[(0, 0)], images_d[(1, 0)], images_d[(2, 0)], images_d[(3, 0)]
)
images_l = list(images_d.values())
sprite = AnimatedSprite(images_l, Vector2(100, 100), anim_layer)

# ---- ticking ----
while True:
    # --- event loop ---
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pg.mouse.get_pos())
            # TODO: Offsetting does not quite work. Let's keep iterating.
            tile = tilemap.world_to_map(mouse_pos)

            print(f"click: {mouse_pos} : {tile} : [{floor(tile.x)},{floor(tile.y)}]")

    sprite.set_image(randint(0, len(sprite.images) - 1))

    # --- render loop ---
    display.fill("darkblue")
    tile_layer.draw(display)
    anim_layer.draw(display)
    pg.display.update()
    clock.tick(60)
