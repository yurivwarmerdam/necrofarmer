from game_scripts.game_ui import MainUI
from scripts.custom_sprites import integer_scale
from scripts.ui_shim import UIButton


import pygame as pg


class ContextPanel:
    """
    This should be passed MainUi.
    MainUI is expected to contain portrait panel and context panel.
    Portrait gives either big image, or a series of small thumbs.
    context is contextual, based on what's selected.
    """

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