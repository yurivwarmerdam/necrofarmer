from scripts.custom_sprites import integer_scale
from scripts.ui_shim import UIButton, UIPanel
from pygame_gui.core.interfaces.container_interface import IContainerAndContainerLike
from abc import ABC, abstractmethod

import pygame as pg


class ContextPanel(ABC):
    """
    Portrait gives either big image, or a series of small thumbs.
    context is contextual, based on what's selected.
    """

    def __init__(
        self, *, portait_id: str = "default", context_panel_size: pg.Rect
    ) -> None:
        self.portait_id: str = portait_id
        self._context_panel: UIPanel = UIPanel(context_panel_size)
        pass

    @property
    # @abstractmethod
    def portrait_button(self) -> UIButton:
        return UIButton(
            pg.Rect(3, 3, 54 * 3, 46 * 3),
            text="",
            object_id=self.portait_id,
            scale_func=integer_scale,
        )

    @property
    # @abstractmethod
    def context_panel(self) -> UIPanel:
        return self._context_panel
        pass

    @abstractmethod
    def set_context_elems(self, context_container: IContainerAndContainerLike):
        pass
