import pygame as pg
from typing import Dict
from pygame_gui.core import ObjectID, UIElement
from pygame_gui.core.interfaces import (
    IContainerLikeInterface,
    IUIElementInterface,
    IUIManagerInterface,
)
from pygame_gui.elements import UIImage
from pygame.rect import Rect, FRect
from scripts.custom_sprites import tilingscale, ninepatchscale, integer_scale
from scripts.utils import load_image, sheet_to_sprites, sheet_to_sprite
from functools import partial
from pygame import Vector2
from blinker import signal
from game_scripts.commander import Commander
from pygame.sprite import Group
import pygame_gui
from scripts.ui_shim import UIButton, UIPanel
import pygame


# This should be a container object; not a uipanel.
# Can definitely hold a bunch of utility functions.
class MainUI:
    def __init__(self):
        # setup main elements

        nine_slice_func = partial(
            ninepatchscale, patch_margain=3, scale_func=tilingscale
        )
        portrait_panel_rect: Rect = Rect(0, 0, 170, 146)
        context_panel_rect: Rect = Rect(0, 0, 400, 99)
        ui_components_sheet = load_image("art/ui_components.png")
        ui_background_sprite = sheet_to_sprite(ui_components_sheet, Rect(0, 0, 60, 62))
        # ui_background_sprite = sheet_to_sprite(ui_components_sheet, Rect(132, 5, 61, 22))

        # ------- base elements -------

        self.portrait_panel = UIPanel(
            pg.Rect(
                0,
                -portrait_panel_rect[3],
                portrait_panel_rect[2],
                portrait_panel_rect[3],
            ),
            anchors={
                "left": "left",
                "right": "left",
                "top": "bottom",
                "bottom": "bottom",
            },
            object_id="#portrait_background",
        )
        # portrait_background = UIImage(
        #     portrait_panel_rect,
        #     portrait_background_sprite,
        #     anchors={
        #         "left": "left",
        #         "right": "right",
        #         "top": "top",
        #         "bottom": "bottom",
        #     },
        #     container=portrait_panel.get_container(),
        # )
        # print(portrait_panel.rect)

        self.context_background = UIPanel(
            pg.Rect(
                portrait_panel_rect[2],
                -(context_panel_rect[3]),
                context_panel_rect[2],
                context_panel_rect[3],
            ),
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
            # object_id="#panel_background",
            scale_func=nine_slice_func,
        )
        UIImage(
            context_panel_rect,
            ui_background_sprite,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
            scale_func=nine_slice_func,
            container=self.context_background.get_container(),
        )

        self.context_panel = UIPanel(
            pg.Rect(
                portrait_panel_rect[2] - 2,
                -(context_panel_rect[3] - 1),
                context_panel_rect[2],
                context_panel_rect[3],
            ),
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
        )

        # signals we are observing
        selected_changed = signal("selected_changed")
        selected_changed.connect(self.selected_changed, weak=False)

    def selected_changed(self, sender: Commander):
        # create appropriate contextpanel, depending on what is selected
        print(f"changing selected. Sender: {sender}")
        if sender.selected:
            self.active_panel = ContextPanel(self)
        else:
            if self.active_panel:
                self.active_panel = None
                self.portrait_panel.get_container().clear()
                self.context_panel.get_container().clear()
        for i in sender.selected:
            print(type(i))


# This should be passed portrait panel and context panel. Portrait gives either big image, or a series of small thumbs.
# context is contextual, based on what's selected.
class ContextPanel:
    def __init__(self, main_ui: MainUI):
        portrait_button = UIButton(
            pg.Rect(3, 3, 54 * 3, 46 * 3),
            text="",
            object_id="#thopter_button",
            scale_func=integer_scale,
            container=main_ui.portrait_panel.get_container(),
        )

        image_button = UIButton(
            pg.Rect(3, 3, 54, 46),
            text="",
            object_id="#thopter_button",
            scale_func=integer_scale,
            container=main_ui.context_panel.get_container(),
        )
