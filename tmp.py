from typing import Dict, Iterable
import pygame as pg
from pygame import Surface
from pygame.constants import BUTTON_LEFT as BUTTON_LEFT
import pygame_gui
from pygame_gui.core import ObjectID, UIElement
from pygame_gui.core.interfaces import (
    IContainerLikeInterface,
    IUIElementInterface,
    IUIManagerInterface,
)
from scripts.utils import load_image, sheet_to_sprites
from pygame.math import Vector2
import sys
from typing import Tuple
from pygame import Rect
from pygame.sprite import Sprite, Group
from scripts.custom_sprites import NodeSprite
# from scripts import camera


class SelectBox(NodeSprite):
    def __init__(self) -> None:
        super().__init__(Surface((0, 0)))
        self.color = pg.Color(34, 135, 34)
        self.image.fill(self.color)
        self.image.set_alpha(128)
        self.dragging: bool = False
        self.start = Vector2()
        # self.camera = camera.get_camera()

    def start_drag(self):
        self.start = pg.mouse.get_pos()
        self.dragging = True

    def stop_drag(self):
        self.image = pg.Surface((0, 0))
        self.dragging = False

    def update(self, _delta=0.0):
        if self.dragging:
            mouse = pg.mouse.get_pos()
            tl = (min(self.start[0], mouse[0]), min(self.start[1], mouse[1]))
            size = (
                abs(self.start[0] - pg.mouse.get_pos()[0]),
                abs(self.start[1] - pg.mouse.get_pos()[1]),
            )
            # print(f"dragging: {size}")
            self.image = Surface(size)
            self.image.set_alpha(128)
            self.rect = self.image.get_rect()
            self.pos = tl
            self.image.fill(self.color)
            pg.draw.rect(
                self.image, "darkgreen", self.rect.move(-self.rect.x, -self.rect.y), 1
            )
        else:
            self.rect = Rect(50, 50, 0, 0)


pg.init()

my_group = Group()
resolution = (636, 333)
manager = pygame_gui.UIManager(resolution)

display: Surface = pg.display.set_mode(resolution, pg.SCALED)

background = pg.Surface(resolution)
background.fill(pg.Color("lightblue"))

ui_image = load_image("art/tst_ui.png")
button_sprites = sheet_to_sprites(load_image("art/thumbnails.png"), Vector2(46, 38))
outline_sprites = sheet_to_sprites(load_image("art/outlines.png"), Vector2(54, 46))
clock = pg.time.Clock()

# a_rect = pg.Rect(0, 0, 0, 0)

# start = Rect(50, 50, 0, 0)

fps_list = list(range(60))
fps_counter = pygame_gui.elements.UITextBox("text", Rect(5, 5, 100, 30))

box = SelectBox()

box_group = Group()
box_group.add(box)

while True:
    time_delta = clock.tick() / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()
        else:
            pass

        processed = manager.process_events(event)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            box.start_drag()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            box.stop_drag()

    box.update()

    display.blit(background, (0, 0))
    box_group.draw(display)
    # --- fps stuff ---

    manager.update(time_delta)

    fps_list.pop(0)
    fps_list.append(time_delta)
    asd = [1 / i for i in fps_list]
    fps_counter.set_text(str(round(sum(asd) / len(asd))))

    manager.draw_ui(display)

    # --- /fps stuff ---

    pg.display.update()
