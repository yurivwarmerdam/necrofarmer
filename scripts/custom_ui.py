from typing import Dict

import pygame as pg
from pygame.transform import smoothscale
import pygame_gui
from scripts.ui_shim import UIPanel
from pygame_gui.core import IContainerLikeInterface, ObjectID, UIElement
from pygame_gui.core.interfaces import IUIElementInterface, IUIManagerInterface
from scripts.custom_sprites import ninepatchscale, tilingscale
from functools import partial
from pygame_gui.elements import UIImage


NINE_SLICE_FUNC = partial(ninepatchscale, patch_margain=3, scale_func=tilingscale)


class ImagePanel(UIPanel):
    def __init__(
        self,
        relative_rect: pg.Rect | pg.FRect,
        starting_height: int = 1,
        manager: IUIManagerInterface | None = None,
        *,
        element_id: str = "panel",
        margins: Dict[str, int] | None = None,
        container: IContainerLikeInterface | None = None,
        parent_element: UIElement | None = None,
        object_id: ObjectID | str | None = None,
        anchors: Dict[str, str | IUIElementInterface] | None = None,
        visible: int = 1,
        scale_func=pg.transform.smoothscale,
        image_surf: pg.Surface = pg.Surface((0, 0)),
    ):
        super().__init__(
            relative_rect,
            starting_height,
            manager,
            element_id=element_id,
            margins=margins,
            container=container,
            parent_element=parent_element,
            object_id=object_id,
            anchors=anchors,
            visible=visible,
            # scale_func=scale_func,
        )
        self.image_surf = UIImage(
            relative_rect.move(-relative_rect.x, -relative_rect.y),
            image_surf,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
            scale_func=scale_func,
            container=self.get_container(),
        )
