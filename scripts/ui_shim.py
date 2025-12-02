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
    if dest_surface is not None:
        if dest_surface.size != size:
            raise ValueError("Destination surface doesn't match the provided size")
    else:
        dest_surface = Surface(size)
    for x in range(0, dest_surface.width, surface.width):
        for y in range(0, dest_surface.height, surface.height):
            dest_surface.blit(surface, (x, y))
    return dest_surface


def ninepatchscale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
    patch_margain: dict | int = {"left": 0, "right": 0, "top": 0, "bottom": 0},
    scale_func=pygame.transform.scale,
) -> Surface:
    """
    Behaves like a scaling func, but should probably be thought of more as a wrapper for some other scaling func.
    """
    if dest_surface is not None:
        if dest_surface.size != size:
            raise ValueError("Destination surface doesn't match the provided size")
    else:
        dest_surface = Surface(size)

    if type(patch_margain) is int:
        patch_margain = {
            "left": patch_margain,
            "right": patch_margain,
            "top": patch_margain,
            "bottom": patch_margain,
        }

    if not dest_surface:
        dest_surface = Surface(size)

    surface_w, surface_h = surface.size
    dest_w, dest_h = size  # non-sequence argument caught by python
    subsurface = surface.subsurface

    surf_center_w = surface_w - (patch_margain["left"] + patch_margain["right"])
    surf_center_h = surface_h - (patch_margain["top"] + patch_margain["bottom"])

    dest_center_w = dest_w - (patch_margain["left"] + patch_margain["right"])
    dest_center_h = dest_h - (patch_margain["top"] + patch_margain["bottom"])

    if (
        min(patch_margain.values()) < 0
        or patch_margain["left"] + patch_margain["right"] > dest_w
        or patch_margain["top"] + patch_margain["bottom"] > dest_h
    ):
        raise ValueError(
            "Corner size must be nonnegative and not greater than the smaller between width and height"
        )
    if not any(patch_margain.values()):  # default to normal scaling if all are 0
        return scale_func(surface, size)

    dest_surface.blit(  # topleft corner
        subsurface(0, 0, patch_margain["left"], patch_margain["top"]), (0, 0)
    )
    dest_surface.blit(  # topright corner
        subsurface(
            surface_w - patch_margain["right"],
            0,
            patch_margain["right"],
            patch_margain["top"],
        ),
        (dest_w - patch_margain["right"], 0),
    )
    dest_surface.blit(  # bottomleft corner
        subsurface(
            0,
            surface_h - patch_margain["bottom"],
            patch_margain["left"],
            patch_margain["bottom"],
        ),
        (0, dest_h - patch_margain["bottom"]),
    )
    dest_surface.blit(  # bottomright corner
        subsurface(
            surface_w - patch_margain["right"],
            surface_h - patch_margain["bottom"],
            patch_margain["right"],
            patch_margain["bottom"],
        ),
        (dest_w - patch_margain["right"], dest_h - patch_margain["bottom"]),
    )

    if patch_margain["top"] > 0:
        dest_surface.blit(  # top side
            scale_func(
                subsurface(
                    patch_margain["left"],
                    0,
                    surf_center_w,
                    patch_margain["top"],
                ),
                (dest_center_w, patch_margain["top"]),
            ),
            (patch_margain["left"], 0),
        )
    if patch_margain["bottom"] > 0:
        dest_surface.blit(  # bottom side
            scale_func(
                subsurface(
                    patch_margain["left"],
                    surface_h - patch_margain["bottom"],
                    surf_center_w,
                    patch_margain["bottom"],
                ),
                (dest_center_w, patch_margain["bottom"]),
            ),
            (patch_margain["left"], dest_h - patch_margain["bottom"]),
        )

    if patch_margain["left"] > 0:
        dest_surface.blit(  # left side
            scale_func(
                subsurface(
                    0,
                    patch_margain["top"],
                    patch_margain["left"],
                    surf_center_h,
                ),
                (patch_margain["left"], dest_center_h),
            ),
            (0, patch_margain["top"]),
        )
    if patch_margain["right"] > 0:
        dest_surface.blit(  # right side
            scale_func(
                subsurface(
                    surface_w - patch_margain["right"],
                    patch_margain["top"],
                    patch_margain["right"],
                    surf_center_h,
                ),
                (patch_margain["right"], dest_center_h),
            ),
            (dest_w - patch_margain["right"], patch_margain["top"]),
        )

    if surf_center_w > 0 and surf_center_h > 0:
        dest_surface.blit(  # central area
            scale_func(
                subsurface(
                    patch_margain["left"],
                    patch_margain["top"],
                    surf_center_w,
                    surf_center_h,
                ),
                (dest_center_w, dest_center_h),
            ),
            (patch_margain["left"], patch_margain["top"]),
        )

    return dest_surface
