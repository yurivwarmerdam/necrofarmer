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
        self.draging:bool = False
        self.drag_start:Vector2|None = None
        self.rect:Rect = Rect()

    def update(self, _delta=0.0):
        self.rect.bottomright =  pg.mouse.get_pos()
        pass

    def start_drag(self):
        self.draging=True
        self.rect.topleft=pg.mouse.get_pos()


pg.init()

resolution = (636, 333)

display: Surface = pg.display.set_mode(resolution, pg.SCALED)

background = pg.Surface(resolution)
background.fill(pg.Color("lightblue"))

ui_image = load_image("art/tst_ui.png")
button_sprites = sheet_to_sprites(load_image("art/thumbnails.png"), Vector2(46, 38))
outline_sprites = sheet_to_sprites(load_image("art/outlines.png"), Vector2(54, 46))
clock = pg.time.Clock()

a_rect=pg.Rect(50,50,50,50)

start=(50,50)

while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()
        else:
            pass

        if event.type in [
            pg.MOUSEBUTTONUP,
            pygame_gui.UI_BUTTON_PRESSED,
            pg.MOUSEBUTTONDOWN,
        ]:
            pass
            # print(processed, pg.event.event_name(event.type))
    display.blit(background, (0, 0))

    tl = start
    br = pg.mouse.get_pos()


    #ok, either: sort x coords, and y coords, and redistribute
    #or: take the union of 2 rects of size 0 at pos start and mouse_pos
    # How do I speeds test this?? Just fps counter, maybe.
    a_rect.update(*tl,br[0]-tl[0],br[1]-tl[0])


    # a_rect.bottomright=pg.mouse.get_pos()

    pg.draw.rect(display,"darkgreen",a_rect,1)

    pg.display.update()

# Ok, so mouse events get consumed. That's good.
# Now to figure out if that also happens when dealingw ith other ui elems.
# Start ehre: https://github.com/MyreMylar/pygame_gui_examples
# FOUND IT: https://github.com/MyreMylar/tower_defence
# Thought: Have my own UIPanel element that serves to:
#   - draw a picture
#   - consume clicks if the mouse pos overlaps
# Another thought: Maybe only draw a subset of the world the should actually be visile?
