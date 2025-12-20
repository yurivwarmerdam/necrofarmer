import warnings
from typing import Any
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
from pygame_gui.core.ui_appearance_theme import (
    UIAppearanceTheme as UIAppearanceTheme_original,
)
from pygame_gui import ui_manager


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


class UIAppearanceTheme(UIAppearanceTheme_original):
    def merge_images_by_layer(self, element_list, prototype_list):
        by_layer = {img["layer"]: img for img in prototype_list}
        for img in element_list:
            by_layer[img["layer"]] = img
        return sorted(by_layer.values(), key=lambda x: x["layer"])

    def merge_dicts(self, element, prototype):
        result = dict(prototype)

        for key, value in element.items():
            if key not in prototype:
                result[key] = value
                continue

            if isinstance(value, dict) and isinstance(prototype[key], dict):
                result[key] = self.merge_dicts(value, prototype[key])

            elif isinstance(value, list) and key.endswith("_images"):
                result[key] = self.merge_images_by_layer(value, prototype[key])

            else:
                result[key] = value

        return result

    def _parse_theme_data_from_json_dict(self, theme_dict: dict[str, Any]) -> None:
        # Validate theme data before processing
        validation_errors = self.validate_theme_data(theme_dict)
        if validation_errors:
            warnings.warn(
                f"Theme validation found {len(validation_errors)} errors:\n"
                + "\n".join(f"  - {error}" for error in validation_errors),
                UserWarning,
            )

        # Load default colors first if they exist
        if "defaults" in theme_dict:
            self._load_colour_defaults_from_theme(theme_dict)

        for element_name in theme_dict:
            self._load_prototype(element_name, theme_dict)
            element_theming = theme_dict[element_name]
            if "prototype" in element_theming:
                element_theming = self.merge_dicts(
                    element_theming, theme_dict[element_theming["prototype"]]
                )
            self._parse_single_element_data(element_name, element_theming)

        self._load_fonts_images_and_shadow_edges()

    pass
    # def _parse_single_element_data(
    #     self, element_name: str, element_theming: dict[str, Any]
    # ) -> None:
    #     # Clear image data if no images block is present in the new theme
    #     # This ensures proper cleanup when switching to themes without images
    #     if "images" not in element_theming and "prototype" not in element_theming:
    #         if element_name in self.ui_element_image_locs:
    #             self.ui_element_image_locs[element_name].clear()
    #         if element_name in self.ui_element_image_surfaces:
    #             self.ui_element_image_surfaces[element_name].clear()

    #     for data_type in element_theming:
    #         if data_type == "font":
    #             file_dict = element_theming[data_type]
    #             if isinstance(file_dict, list):
    #                 for item in file_dict:
    #                     self._load_element_font_data_from_theme(item, element_name)
    #             else:
    #                 self._load_element_font_data_from_theme(file_dict, element_name)

    #         if data_type in ["colours", "colors"]:
    #             self._load_element_colour_data_from_theme(
    #                 data_type, element_name, element_theming
    #             )

    #         elif data_type == "images":
    #             self._load_element_image_data_from_theme(
    #                 data_type, element_name, element_theming
    #             )

    #         elif data_type == "misc":
    #             self._load_element_misc_data_from_theme(
    #                 data_type, element_name, element_theming
    #             )

    # def _parse_single_element_data(
    #     self, element_name: str, element_theming: dict[str, Any]
    # ) -> None:
    #     # Clear image data if no images block is present in the new theme
    #     # This ensures proper cleanup when switching to themes without images
    #     if element_name == "#inherited":
    #         print("here we go again")
    #     if "images" not in element_theming:
    #         if element_name in self.ui_element_image_locs:
    #             self.ui_element_image_locs[element_name].clear()
    #         if element_name in self.ui_element_image_surfaces:
    #             self.ui_element_image_surfaces[element_name].clear()

    #     for data_type in element_theming:
    #         if data_type == "font":
    #             file_dict = element_theming[data_type]
    #             if isinstance(file_dict, list):
    #                 for item in file_dict:
    #                     self._load_element_font_data_from_theme(item, element_name)
    #             else:
    #                 self._load_element_font_data_from_theme(file_dict, element_name)

    #         if data_type in ["colours", "colors"]:
    #             self._load_element_colour_data_from_theme(
    #                 data_type, element_name, element_theming
    #             )

    #         elif data_type == "images":
    #             self._load_element_image_data_from_theme(
    #                 data_type, element_name, element_theming
    #             )

    #         elif data_type == "misc":
    #             self._load_element_misc_data_from_theme(
    #                 data_type, element_name, element_theming
    #             )


ui_manager.UIAppearanceTheme = UIAppearanceTheme


class UIManager(ui_manager.UIManager):
    pass


# ------------------------------------
# my_framework_module.py
# This file replaces/extends framework.framework_module

# import framework.framework_module as orig
# import framework.internal as internal


# class FixedInternal(internal.internal_class):
#     def do_something(self):
#         # fixed behavior
#         pass


# # override the symbol USED by framework_module
# orig.internal_class = FixedInternal


# class framework_class(orig.framework_class):
#     pass
