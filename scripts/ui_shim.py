from pygame_gui.elements import UIPanel as UIPANEL_original
from pygame_gui.elements import UIImage as UIImage_original
from pygame_gui.core.gui_type_hints import RectLike

import pygame
from typing import Optional, Union
from pygame_gui.core.interfaces import (
    IContainerLikeInterface,
    IUIManagerInterface,
    IUIElementInterface,
)
from pygame_gui.core import UIElement
from pygame_gui.core import ObjectID


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

