import pygame as pg
from typing import Dict
from pygame_gui.core import ObjectID, UIElement
from pygame_gui.core.interfaces import (
    IContainerLikeInterface,
    IUIElementInterface,
    IUIManagerInterface,
)
from pygame_gui.elements import UIImage, UIPanel
from pygame.rect import Rect, FRect
from scripts.custom_sprites import tilingscale, ninepatchscale
from scripts.utils import load_image, sheet_to_sprites
from functools import partial
from scripts.ui import ImageButton
from pygame import Vector2
from blinker import signal
from game_scripts.commander import Commander
from pygame.sprite import Group


class MainUI(UIPanel):
    def __init__(self):
        context_panel_size = (300, 80)
        super().__init__(
            pg.Rect(80, -context_panel_size[1], *context_panel_size),
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
        )
        # setup main elements

        scale_func = partial(ninepatchscale, patch_margain=3, scale_func=tilingscale)
        context_panel_rect: Rect = Rect(0, 0, 400, 100)
        ui_image = load_image("art/tst_ui.png")
        outline_sprites = sheet_to_sprites(
            load_image("art/outlines.png"), Vector2(54, 46)
        )
        button_sprites = sheet_to_sprites(
            load_image("art/thumbnails.png"), Vector2(46, 38)
        )

        # context background?
        image_elem = UIImage(
            context_panel_rect,
            ui_image,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
            scale_func=scale_func,
            container=self.get_container(),
        )
        pass
        ImageButton(
            (2, 2),
            outline_sprites,
            button_sprites[(0, 0)],
            container=self.get_container(),
        )

        # signals we are observing
        selected_changed = signal("selected_changed")
        selected_changed.connect(self.selected_changed)

    def selected_changed(self, sender: Group, **kwargs):
        # create appropriate contextpanel, depending on what is selected
        print(f"changing selected. Sender: {sender}")
        for i in sender:
            print(type(i))


class ContextPanel(UIPanel):
    pass
