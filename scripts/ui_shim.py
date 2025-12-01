from pygame_gui.elements import UIPanel as UIPANEL_original
from pygame_gui.elements import UIImage as UIImage_original
from pygame_gui.core.gui_type_hints import RectLike

import pygame
from pygame import Surface, Rect
from typing import Optional, Union
from pygame_gui.core.interfaces import (
    IContainerLikeInterface,
    IUIManagerInterface,
    IUIElementInterface,
)
from pygame_gui.core import UIElement
from pygame_gui.core import ObjectID
from pygame.typing import Point


class UIPanel(UIPANEL_original):
    """
    A shim until my PR gets accepted.
    """

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Can be overridden, also handle resizing windows. Gives UI Windows access to pygame events.
        Currently just blocks mouse click down events from passing through the panel.

        :param event: The event to process.

        :return: Should return True if this element consumes this event.

        """
        consumed_event = False
        if (
            self is not None
            and event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
            and event.button
            in [pygame.BUTTON_LEFT, pygame.BUTTON_RIGHT, pygame.BUTTON_MIDDLE]
        ):
            scaled_mouse_pos = self.ui_manager.calculate_scaled_mouse_position(
                event.pos
            )
            if self.hover_point(scaled_mouse_pos[0], scaled_mouse_pos[1]):
                consumed_event = True

        return consumed_event


class UIImage(UIImage_original):
    def __init__(
        self,
        relative_rect: RectLike,
        image_surface: pygame.surface.Surface,
        manager: Optional[IUIManagerInterface] = None,
        image_is_alpha_premultiplied: bool = False,
        container: Optional[IContainerLikeInterface] = None,
        parent_element: Optional[UIElement] = None,
        object_id: Optional[Union[ObjectID, str]] = None,
        anchors: Optional[dict[str, Union[str, IUIElementInterface]]] = None,
        visible: int = 1,
        *,
        starting_height: int = 1,
        scale_func=pygame.transform.smoothscale,
        nineslice={},
    ):
        super().__init__(
            relative_rect,
            image_surface,
            manager,
            image_is_alpha_premultiplied,
            container,
            parent_element,
            object_id,
            anchors,
            visible,
            starting_height=starting_height,
            scale_func=scale_func,
        )
        self.nineslice = nineslice


def tilingscale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Scale a surface to an arbitrary size smoothly.

    tiles the input surface as a way of scaling each dimension as required.
    For shrinkage, the surface is simply clipped to fit the dest_surface.
    The size is a 2 number sequence for (width, height).

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must be the same as the size (width, height) passed
    in, and the same depth and format as the source Surface.
    """
    if not dest_surface:
        dest_surface = Surface(size)
    for x in range(0, dest_surface.width, surface.width):
        for y in range(0, dest_surface.height, surface.height):
            dest_surface.blit(surface, (x, y))
    return dest_surface


def ninepatchscale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
    patch_margain={"left": 0, "right": 0, "top": 0, "bottom": 0},
) -> Surface:
    """
    Behaves like a scaling func, but should probably be thought of more as a wrapper for some other scaling func.
    """
    if not dest_surface:
        dest_surface = Surface(size)

    tl_dim = Surface((patch_margain["left"], patch_margain["top"]))
    tr_dim = Surface((patch_margain["right"], patch_margain["top"]))
    bl_dim = Surface((patch_margain["left"], patch_margain["bottom"]))
    br_dim = Surface((patch_margain["rght"], patch_margain["bottom"]))

    center_dim = dest_surface.get_rect().copy()
    center_dim.width -= patch_margain["left"] + patch_margain["right"]
    center_dim.height -= patch_margain["top"] + patch_margain["bottom"]
