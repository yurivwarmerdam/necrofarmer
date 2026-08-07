from abc import ABC
from functools import partial
import pygame as pg
from pygame_gui.core import IContainerLikeInterface
from pygame_gui.core.interfaces.container_interface import IContainerAndContainerLike

from scripts.custom_sprites import ninepatchscale, tilingscale
from scripts.custom_ui import ImagePanel
from scripts.ui_shim import UIPanel
from scripts.utils import load_image, sheet_to_sprite


class ContextPanel(ABC):
    """
    Portrait gives either big image, or a series of small thumbs.
    context is contextual, based on what's selected.
    """

    def __init__(
        self,
        *,
        portrait_id: str = "default",
        context_container: IContainerAndContainerLike,
    ) -> None:
        """
        Make sure to set elements inside context_panel of main_ui.

        context_container: context_panel container
        """
        self.portrait_id: str = portrait_id
        self.context_container = context_container

    def update(self, _delta) -> None:
        pass


class BackgroundPanel(UIPanel):
    def __init__(
        self,
        relative_rect: pg.Rect,
        container: IContainerLikeInterface | None = None,
        # parent_element: UIElement | None = None,
        anchors: dict[str, str] = {
            "left": "left",
            "right": "left",
            "top": "top",
            "bottom": "top",
        },
        visible: int = 1,
    ):
        NINE_SLICE_FUNC = partial(
            ninepatchscale, patch_margain=3, scale_func=tilingscale
        )
        super().__init__(
            relative_rect,
            container=container,
            anchors=anchors,
            visible=visible,
            scale_func=NINE_SLICE_FUNC,
        )
        ui_components_sheet = load_image("art/ui_components.png")
        ui_background_sprite = sheet_to_sprite(
            ui_components_sheet, pg.Rect(0, 0, 60, 62)
        )
        self.context_background = ImagePanel(
            relative_rect.move(-relative_rect.x, -relative_rect.y),
            starting_height=0,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
            image_surf=ui_background_sprite,
            scale_func=NINE_SLICE_FUNC,
            container=self.get_container(),
            visible=visible,
        )


