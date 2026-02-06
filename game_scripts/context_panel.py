from scripts.custom_sprites import integer_scale
from scripts.ui_shim import UIButton
from abc import ABC, abstractmethod

import pygame as pg


class ContextPanel(ABC):
    """
    Portrait gives either big image, or a series of small thumbs.
    context is contextual, based on what's selected.
    """

    def __init__(self,portait_id="default") -> None:
        self._portrait_button = UIButton(
            pg.Rect(3, 3, 54 * 3, 46 * 3),
            text="",
            object_id=portait_id,
            scale_func=integer_scale,
            # container=main_ui.portrait_panel.get_container(),
        )
        # self._image_button = UIButton(
        #     pg.Rect(3, 3, 54, 46),
        #     text="",
        #     # object_id="#thopter_button",
        #     scale_func=integer_scale,
        #     # container=main_ui.context_panel.get_container(),
        # )
        pass

    @property
    @abstractmethod
    def portrait_button(self) -> UIButton:
        return self._portrait_button

    @property
    @abstractmethod
    def image_button(self) -> UIButton:
        return self._image_button
