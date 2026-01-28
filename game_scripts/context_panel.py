from dataclasses import dataclass
from scripts.custom_sprites import integer_scale
from scripts.ui_shim import UIButton


import pygame as pg


@dataclass
class ContextPanel:
    """
    Portrait gives either big image, or a series of small thumbs.
    context is contextual, based on what's selected.
    """

    portrait_button = UIButton(
        pg.Rect(3, 3, 54 * 3, 46 * 3),
        text="",
        # object_id="#thopter_button",
        scale_func=integer_scale,
        # container=main_ui.portrait_panel.get_container(),
    )
    image_button = UIButton(
        pg.Rect(3, 3, 54, 46),
        text="",
        # object_id="#thopter_button",
        scale_func=integer_scale,
        # container=main_ui.context_panel.get_container(),
    )
