import pygame as pg
from pygame import Vector2, Surface
from pygame.sprite import Group, Sprite
import sys
from scripts.tilemap import Tilemap
from math import floor
from scripts.utils import sheet_to_sprites, load_image
from random import randint


class AnimationSequence:
    def __init__(self, *frames: Surface, frame_time=200) -> None:
        self.frames = frames
        self.frame_time = frame_time
        self.reset()

    def play(self):
        self.playing = True
        # TODO... now what?

    def reset(self):
        self.current_frame_time = 0
        self.idx = 0

    @property
    def image(self):
        return self.frames[self.idx]

    def tick(self, delta):
        self.current_frame_time += delta
        if self.current_frame_time > self.frame_time:
            self.current_frame_time = self.current_frame_time % self.frame_time
            self.idx = (self.idx + 1) % len(self.frames)
            # print(self.idx)
            return self.image


class AnimatedSprite(Sprite):
    def __init__(
        self,
        animations: dict[str, AnimationSequence],
        pos: Vector2,
        *groups,
    ) -> None:
        super().__init__(*groups)
        self.animations = animations
        self.active_animation = next(iter(animations.values()))
        self.image = self.active_animation.image
        self.rect = self.image.get_rect()
        self.pos = pos

    def set_animation(self, name):
        self.active_animation = self.animations[name]
        self.image = self.active_animation.image
        pass

    def update(self, delta) -> None:
        result = self.active_animation.tick(delta)
        if result:
            self.image = result


pg.init()

display = pg.display.set_mode((800, 400), pg.SCALED, pg.RESIZABLE)
clock = pg.time.Clock()

# tilemap
tile_layer = Group()
tilemap = Tilemap("art/tmx/tst_square_map.tmx", {"ground": tile_layer})
anim_layer = Group()

# animated sprite
images_d = sheet_to_sprites(load_image("art/tardigrade.png"), Vector2(80, 80))

seq0 = AnimationSequence(
    images_d[(0, 0)],
    images_d[(1, 0)],
    images_d[(2, 0)],
    images_d[(3, 0)],
)
seq1 = AnimationSequence(
    images_d[(0, 1)],
    images_d[(1, 1)],
    images_d[(2, 1)],
    images_d[(3, 1)],
)
seq2 = AnimationSequence(
    images_d[(0, 2)],
    images_d[(1, 2)],
    images_d[(2, 2)],
    images_d[(3, 2)],
)
seq3 = AnimationSequence(
    images_d[(0, 3)],
    images_d[(1, 3)],
    images_d[(2, 3)],
    images_d[(3, 3)],
)

sprite = AnimatedSprite(
    {"0": seq0, "1": seq1, "2": seq2, "3": seq3}, Vector2(100, 100), anim_layer
)

clock = pg.time.Clock()

# ---- ticking ----
while True:
    _delta = clock.get_time()
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

    # sprite.set_animation(randint(0, len(sprite.animations) - 1))

    if randint(0,100)>99:
        

    # --- update loop ---
    anim_layer.update(_delta)

    # --- render loop ---
    display.fill("darkblue")
    tile_layer.draw(display)
    anim_layer.draw(display)
    pg.display.update()
    clock.tick(60)
