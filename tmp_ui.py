from typing import Dict, Iterable
import pygame as pg
from pygame import Surface, Rect
from pygame.constants import BUTTON_LEFT as BUTTON_LEFT
# import pygame_gui
from scripts import ui_shim
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
from typing import Tuple, Callable, Any


from scripts.ui_shim import UIPanel


class Thing:
    def do_stuff(self):
        print("Goober")


class ImageButton(pygame_gui.elements.UIButton):
    def __init__(
        self,
        pos,
        outline_sprites,
        fill_sprite,
        container: IContainerLikeInterface | None = None,
    ):
        super().__init__(
            relative_rect=outline_sprites[(0, 0)].get_rect(),
            text="",
            object_id="hello_button",
            container=container,
        )
        self.normal_images = [outline_sprites[(0, 0)], fill_sprite]
        self.hovered_images = [outline_sprites[(0, 0)], fill_sprite]
        self.disabled_images = [outline_sprites[(2, 0)], fill_sprite]
        self.selected_images = [outline_sprites[(1, 0)], fill_sprite]
        self.set_relative_position(pos)
        self.rebuild()


class NewButton(pygame_gui.elements.UIButton):
    def __init__(
        self,
        pos: Vector2,
    ):
        object_id = "#thopter_button"
        super().__init__(
            Rect(*pos, 54, 46),
            "",
            object_id=object_id,
        )


class ContextPanel(UIPanel):
    """Good example of being able to nest ui elements."""

    def __init__(self, display: Surface, outline_sprites, my_object):
        screen_size = display.get_size()
        own_size = [450, 100]
        own_rect = pg.Rect(80, screen_size[1] - own_size[1], *own_size)
        super().__init__(
            own_rect,
            element_id="context_panel",
            # anchors=anchors,
        )
        self.image = pg.Surface(self.relative_rect.size)
        self.image.fill(pg.Color("darkgray"))

        self.hello_button = ImageButton(
            (2, 2),
            outline_sprites,
            button_sprites[(0, 0)],
            container=self.get_container(),
        )
        self.hello_button.bind(pygame_gui.UI_BUTTON_PRESSED, my_object.do_stuff)
        self.other_button = ImageButton(
            (58, 2),
            outline_sprites,
            button_sprites[(1, 0)],
            container=self.get_container(),
        )


pg.init()

pg.display.set_caption("Quick Start")

resolution = (636, 333)

display: Surface = pg.display.set_mode(resolution, pg.RESIZABLE)

background = pg.Surface(resolution)
background.fill(pg.Color("springgreen3"))

# manager = pygame_gui.UIManager(resolution, theme_path="theme/theme.json")
manager = ui_shim.UIManager(resolution, theme_path="theme/buttons.json")

ui_image = load_image("art/tst_ui.png")
button_sprites = sheet_to_sprites(load_image("art/thumbnails.png"), Vector2(46, 38))
outline_sprites = sheet_to_sprites(load_image("art/outlines.png"), Vector2(54, 46))


thing = Thing()
ContextPanel(display, outline_sprites, thing)

a_rect = outline_sprites[0, 0].get_rect()
b_rect = pg.Rect(0, 0, 54, 46)
ui_panel = UIPanel(
    b_rect,
    manager=manager,
    anchors={"left": "left", "bottom": "bottom"},
)

# button_layout_rect = pg.Rect(0, 0, 100, 20)
hello_rect = pg.Rect(0, 30, 150, 20)

hello_button = pygame_gui.elements.UIButton(
    hello_rect,
    text="Hello",
    object_id="#boring_button"
    # object_id="moar",
    # anchors={"centerx": "centerx", "bottom": "bottom"},
)
# another_button.set_relative_position((0, -10))
# Oh crickey. It tunrs out that the relative position is only kind of relative...

image_button=pygame_gui.elements.UIButton(
    pg.Rect(180,30,60,60),text="theme image?",
    object_id="#thopter_button"
)

NewButton(Vector2(10, 70))

clock = pg.time.Clock()

while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        processed = manager.process_events(event)

        if event.type in [
            pg.MOUSEBUTTONUP,
            pygame_gui.UI_BUTTON_PRESSED,
            pg.MOUSEBUTTONDOWN,
        ]:
            pass

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
