from typing import Dict
import pygame as pg
from pygame import Surface
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

from scripts.ui_shim import UIPanel


class ContextPanel(UIPanel):
    def __init__(self, display: Surface):
        screen_size = display.get_size()
        own_size = [450, 80]
        own_rect = pg.Rect(80, screen_size[1] - own_size[1], *own_size)
        super().__init__(
            own_rect,
            element_id="context_panel",
            # anchors=anchors,
        )
        self.image = pg.Surface(self.relative_rect.size)
        self.image.fill(pg.Color("darkgray"))
        
        self.buton = None


pg.init()

pg.display.set_caption("Quick Start")

resolution = (636, 333)

display: Surface = pg.display.set_mode(resolution, pg.SCALED)

background = pg.Surface(resolution)
background.fill(pg.Color("springgreen3"))

manager = pygame_gui.UIManager(resolution)

ContextPanel(display)

ui_image = load_image("art/tst_ui.png")
button_sprites = sheet_to_sprites(load_image("art/thumbnails.png"), Vector2(46, 38))
outline_sprites = sheet_to_sprites(load_image("art/outlines.png"), Vector2(54, 46))


hello_button = pygame_gui.elements.UIButton(
    relative_rect=outline_sprites[(0, 0)].get_rect(), text="", manager=manager
)
hello_button.normal_images = [outline_sprites[(0, 0)], button_sprites[(0, 0)]]
hello_button.hovered_images = [outline_sprites[(0, 0)], button_sprites[(0, 0)]]
hello_button.selected_images = [outline_sprites[(1, 0)], button_sprites[(0, 0)]]
hello_button.disabled_images = [outline_sprites[(2, 0)], button_sprites[(0, 0)]]

hello_button.set_position((60, 50))

hello_button.rebuild()

a_rect = outline_sprites[0, 0].get_rect()
print(a_rect)
b_rect = pg.Rect(0, 0, 54, 46)
ui_panel = UIPanel(
    b_rect,
    manager=manager,
    anchors={"left": "left", "bottom": "bottom"},
)


# button_layout_rect = pg.Rect(0, 0, 100, 20)
button_layout_rect = pg.Rect(0, -30, 150, 20)

shadow = UIPanel(
    button_layout_rect,
    manager=manager,
    anchors={"left": "left", "bottom": "bottom"},
)

another_button = pygame_gui.elements.UIButton(
    button_layout_rect,
    text="Hello",
    manager=manager,
    anchors={"centerx": "centerx", "bottom": "bottom"},
)
# another_button.set_relative_position((0, -10))
# Oh crickey. It tunrs out that the relative position is only kind of relative...

clock = pg.time.Clock()

print(pg.MOUSEBUTTONUP, pygame_gui.UI_BUTTON_PRESSED)

while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print("image pressed")

        processed = manager.process_events(event)

        if event.type in [
            pg.MOUSEBUTTONUP,
            pygame_gui.UI_BUTTON_PRESSED,
            pg.MOUSEBUTTONDOWN,
        ]:
            print(processed, pg.event.event_name(event.type))

    manager.update(time_delta)

    display.blit(background, (0, 0))
    manager.draw_ui(display)

    pg.display.update()

# Ok, so mouse events get consumed. That's good.
# Now to figure out if that also happens when dealingw ith other ui elems.
# Start ehre: https://github.com/MyreMylar/pygame_gui_examples
# FOUND IT: https://github.com/MyreMylar/tower_defence
# Thought: Have my own UIPanel element that serves to:
#   - draw a picture
#   - consume clicks if the mouse pos overlaps
# Another thought: Maybe only draw a subset of the world the should actually be visile?
