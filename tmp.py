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
from pygame.sprite import Sprite


class SelectBox(Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.draging: bool = False
        self.drag_start: Vector2 | None = None
        self.rect: Rect = Rect()

    def update(self, _delta=0.0):
        self.rect.bottomright = pg.mouse.get_pos()
        pass

    def start_drag(self):
        self.draging = True
        self.rect.topleft = pg.mouse.get_pos()


pg.init()

resolution = (636, 333)
manager = pygame_gui.UIManager(resolution)

display: Surface = pg.display.set_mode(resolution, pg.SCALED)

background = pg.Surface(resolution)
background.fill(pg.Color("lightblue"))

ui_image = load_image("art/tst_ui.png")
button_sprites = sheet_to_sprites(load_image("art/thumbnails.png"), Vector2(46, 38))
outline_sprites = sheet_to_sprites(load_image("art/outlines.png"), Vector2(54, 46))
clock = pg.time.Clock()

a_rect = pg.Rect(0, 0, 0, 0)

start = Rect(50, 50, 0, 0)

fps_list = list(range(60))
fps_counter = pygame_gui.elements.UITextBox("text", Rect(5, 5, 100, 30))


while True:
    time_delta = clock.tick() / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()
        else:
            pass

        processed = manager.process_events(event)

        if event.type in [
            pg.MOUSEBUTTONUP,
            pygame_gui.UI_BUTTON_PRESSED,
            pg.MOUSEBUTTONDOWN,
        ]:
            pass
            # print(processed, pg.event.event_name(event.type))

    # ok, either: sort x coords, and y coords, and redistribute
    # or: take the union of 2 rects of size 0 at pos start and mouse_pos

    # not doing anything: ~47 fps

    # solid 45 fps on battery
    mouse_pos_r = pg.Rect(pg.mouse.get_pos(), (0, 0))
    a_rect = start.union(mouse_pos_r)

    # 45~46 fps on battery
    # mo = pg.mouse.get_pos()
    # tl = Vector2(min((start[0], mo[0])),min((start[1], mo[1])))
    # br = Vector2(max((start[0], mo[0])),max((start[1], mo[1])))
    # a_rect.update(tl,br-tl)

    display.blit(background, (0, 0))
    pg.draw.rect(display, "darkgreen", a_rect, 1)

    # --- fps stuff ---

    manager.update(time_delta)

    fps_list.pop(0)
    fps_list.append(time_delta)
    asd = [1 / i for i in fps_list]
    fps_counter.set_text(str(round(sum(asd) / len(asd))))

    manager.draw_ui(display)

    # --- /fps stuff ---

    pg.display.update()
