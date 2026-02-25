import warnings
from typing import Any, Callable, Iterable, Optional, Union

import pygame
from pygame.constants import BUTTON_LEFT as BUTTON_LEFT
from pygame_gui import ui_manager
from pygame_gui.core import ObjectID
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
from pygame_gui.core.interfaces import (
    IContainerLikeInterface,
    IUIElementInterface,
    IUIManagerInterface,
)
from pygame_gui.core.ui_appearance_theme import (
    UIAppearanceTheme as UIAppearanceTheme_original,
)
from pygame_gui.core.ui_element import UIElement
from pygame_gui.elements import UIButton as UIButton_original
from pygame_gui.elements import UIPanel as UIPANEL_original


class UIPanel(UIPANEL_original):
    """
    A shim until my PR gets accepted.
    Over time I am less and less convinced this is desired behavior.
    I may need to register click down in commander, and only fire up behavior on up. That will lead to a more smooth experience.
    """

    def __init__(
        self,
        relative_rect: RectLike,
        starting_height: int = 1,
        manager: Optional[IUIManagerInterface] = None,
        *,
        element_id: str = "panel",
        margins: Optional[dict[str, int]] = None,
        container: Optional[IContainerLikeInterface] = None,
        parent_element: Optional[UIElement] = None,
        object_id: Optional[Union[ObjectID, str]] = None,
        anchors: Optional[dict[str, Union[str, IUIElementInterface]]] = None,
        visible: int = 1,
        scale_func=pygame.transform.smoothscale,
    ):
        self.scale_func = scale_func
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
        )

    @staticmethod
    def _scale_image_to_fit(
        image: pygame.Surface,
        target_size: tuple[int, int],
        scale_func=pygame.transform.smoothscale,
    ) -> pygame.Surface:
        """
        Scale an image to fit within the target size while maintaining aspect ratio.
        The image will be scaled to the largest size that fits within the target dimensions.

        :param image: The image surface to scale.
        :param target_size: The target size (width, height) to fit the image within.
        :return: The scaled image surface.
        """
        if image is None:
            return None

        image_width, image_height = image.get_size()
        target_width, target_height = target_size

        # Calculate scale factors for both dimensions
        scale_x = target_width / image_width
        scale_y = target_height / image_height

        # Use the smaller scale factor to ensure the image fits within the target size
        scale = min(scale_x, scale_y)

        # Calculate new dimensions
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        # Scale the image
        if new_width > 0 and new_height > 0:
            return scale_func(image, (new_width, new_height))
        else:
            return image

    def _set_any_images_from_theme(self) -> bool:
        """
        Grabs background images for this panel from the UI theme if any are set.
        Supports both single image format and multi-image format from JSON,
        but internally always uses lists for consistency.

        :return: True if any of the images have changed since last time they were set.
        """
        changed = False
        new_images = []
        new_positions = []

        # First try to load multi-image format (background_images)
        try:
            image_details = self.ui_theme.get_image_details(
                "background_images", self.combined_element_ids
            )
            new_images = [detail["surface"] for detail in image_details]
            new_positions = [
                detail.get("position", (0.5, 0.5)) for detail in image_details
            ]
        except LookupError:
            # Fall back to single image format (background_image)
            try:
                image_details = self.ui_theme.get_image_details(
                    "background_image", self.combined_element_ids
                )
                if image_details:
                    new_images = [detail["surface"] for detail in image_details]
                    new_positions = [
                        detail.get("position", (0.5, 0.5)) for detail in image_details
                    ]
            except LookupError:
                # No image found for this state
                pass

        # Apply auto-scaling if enabled
        if new_images and self.auto_scale_images:
            scaled_images = []
            for img in new_images:
                scaled_img = self._scale_image_to_fit(
                    img, self.rect.size, self.scale_func
                )
                scaled_images.append(scaled_img)
            new_images = scaled_images

        # Ensure we have positions for all images (default to center if missing)
        while len(new_positions) < len(new_images):
            new_positions.append((0.5, 0.5))

        # Check if images or positions have changed
        if (
            new_images != self.background_images
            or new_positions != self.background_image_positions
        ):
            self.background_images = new_images
            self.background_image_positions = new_positions
            changed = True

        return changed

    def set_dimensions(self, dimensions: Coordinate, clamp_to_container: bool = False):
        """
        Set the size of this panel and then re-sizes and shifts the contents of the panel container
        to fit the new size.

        :param dimensions: The new dimensions to set.
        :param clamp_to_container: Whether we should clamp the dimensions to the
                                   dimensions of the container or not.

        """
        # Don't use a basic gate on this set dimensions method because the container may be a
        # different size to the window
        super().set_dimensions(dimensions)

        # Handle auto-scaling of background images when panel size changes
        if self.auto_scale_images and self.background_images:
            scaled_images = []
            for img in self.background_images:
                scaled_img = self._scale_image_to_fit(
                    img, self.rect.size, self.scale_func
                )
                scaled_images.append(scaled_img)
            self.background_images = scaled_images
            self.rebuild()

        new_container_dimensions = (
            self.relative_rect.width
            - (self.container_margins["left"] + self.container_margins["right"]),
            self.relative_rect.height
            - (self.container_margins["top"] + self.container_margins["bottom"]),
        )
        if new_container_dimensions != self.get_container().get_size():
            self.get_container().set_dimensions(new_container_dimensions)

    def set_background_images(self, images: list[pygame.Surface]):
        """
        Set the background images for the panel.

        :param images: List of pygame.Surface objects to use as background images
        """
        if images != self.background_images:
            self.background_images = images.copy() if images else []

            # Apply auto-scaling if enabled
            if self.background_images and self.auto_scale_images:
                scaled_images = []
                for img in self.background_images:
                    scaled_img = self._scale_image_to_fit(
                        img, self.rect.size, self.scale_func
                    )
                    scaled_images.append(scaled_img)
                self.background_images = scaled_images

            self.rebuild()

    def set_auto_scale_images(self, auto_scale: bool):
        """
        Enable or disable automatic scaling of background images to fit the panel size.

        :param auto_scale: True to enable auto-scaling, False to disable
        """
        if auto_scale != self.auto_scale_images:
            self.auto_scale_images = auto_scale

            # If enabling auto-scale, rescale existing images
            if auto_scale and self.background_images:
                scaled_images = []
                for img in self.background_images:
                    scaled_img = self._scale_image_to_fit(
                        img, self.rect.size, self.scale_func
                    )
                    scaled_images.append(scaled_img)
                self.background_images = scaled_images
                self.rebuild()

    def add_background_image(self, image: pygame.Surface):
        """
        Add a background image to the panel's image list.

        :param image: pygame.Surface object to add to the background images
        """
        if image is not None:
            # Apply auto-scaling if enabled
            if self.auto_scale_images:
                image = self._scale_image_to_fit(image, self.rect.size, self.scale_func)

            self.background_images.append(image)
            self.rebuild()

    # def process_event(self, event: pygame.event.Event) -> bool:
    #     """
    #     Can be overridden, also handle resizing windows. Gives UI Windows access to pygame events.
    #     Currently just blocks mouse click down events from passing through the panel.

    #     :param event: The event to process.

    #     :return: Should return True if this element consumes this event.

    #     """
    #     consumed_event = False
    #     if (
    #         self is not None
    #         and event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
    #         and event.button
    #         in [pygame.BUTTON_LEFT, pygame.BUTTON_RIGHT, pygame.BUTTON_MIDDLE]
    #     ):
    #         scaled_mouse_pos = self.ui_manager.calculate_scaled_mouse_position(
    #             event.pos
    #         )
    #         if self.hover_point(scaled_mouse_pos[0], scaled_mouse_pos[1]):
    #             consumed_event = True

    #     return consumed_event


class UIButton(UIButton_original):
    def __init__(
        self,
        relative_rect: Union[RectLike, Coordinate],
        text: str,
        manager: Optional[IUIManagerInterface] = None,
        container: Optional[IContainerLikeInterface] = None,
        tool_tip_text: Union[str, None] = None,
        starting_height: int = 1,
        parent_element: Optional[UIElement] = None,
        object_id: Union[ObjectID, str, None] = None,
        anchors: Optional[dict[str, Union[str, IUIElementInterface]]] = None,
        allow_double_clicks: bool = False,
        generate_click_events_from: Iterable[int] = frozenset([pygame.BUTTON_LEFT]),
        visible: int = 1,
        *,
        command: Optional[Union[Callable, dict[int, Callable]]] = None,
        tool_tip_object_id: Optional[ObjectID] = None,
        text_kwargs: Optional[dict[str, str]] = None,
        tool_tip_text_kwargs: Optional[dict[str, str]] = None,
        max_dynamic_width: Optional[int] = None,
        scale_func=pygame.transform.smoothscale,
    ):
        self.scale_func = scale_func
        super().__init__(
            relative_rect,
            text,
            manager,
            container,
            tool_tip_text,
            starting_height,
            parent_element,
            object_id,
            anchors,
            allow_double_clicks,
            generate_click_events_from,
            visible,
            command=command,
            tool_tip_object_id=tool_tip_object_id,
            text_kwargs=text_kwargs,
            tool_tip_text_kwargs=tool_tip_text_kwargs,
            max_dynamic_width=max_dynamic_width,
        )

    @staticmethod
    def _scale_image_to_fit(
        image: pygame.Surface,
        target_size: tuple[int, int],
        scale_func=pygame.transform.smoothscale,
    ) -> pygame.Surface:
        """
        Scale an image to fit within the target size while maintaining aspect ratio.
        The image will be scaled to the largest size that fits within the target dimensions.

        :param image: The image surface to scale.
        :param target_size: The target size (width, height) to fit the image within.
        :return: The scaled image surface.
        """
        if image is None:
            return None

        image_width, image_height = image.get_size()
        target_width, target_height = target_size

        # Calculate scale factors for both dimensions
        scale_x = target_width / image_width
        scale_y = target_height / image_height

        # Use the smaller scale factor to ensure the image fits within the target size
        scale = min(scale_x, scale_y)

        # Calculate new dimensions
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        # Scale the image
        if new_width > 0 and new_height > 0:
            return scale_func(image, (new_width, new_height))
        else:
            return image

    def _set_any_images_from_theme(self) -> bool:
        """
        Grabs images for this button from the UI theme if any are set.
        Supports both single image format and multi-image format from JSON,
        but internally always uses lists for consistency.

        :return: True if any of the images have changed since last time they were set.
        """
        changed = False

        # Process normal state first to establish baseline for fallbacks
        normal_images = []
        normal_positions = []

        # First try to load multi-image format for normal state
        try:
            image_details = self.ui_theme.get_image_details(
                "normal_images", self.combined_element_ids
            )
            normal_images = [detail["surface"] for detail in image_details]
            normal_positions = [detail["position"] for detail in image_details]
        except LookupError:
            # Fall back to single image format for normal state
            try:
                image_details = self.ui_theme.get_image_details(
                    "normal_image", self.combined_element_ids
                )
                if image_details:
                    normal_images = [detail["surface"] for detail in image_details]
                    normal_positions = [detail["position"] for detail in image_details]
            except LookupError:
                # No normal image found
                pass

        # Apply auto-scaling to normal images if enabled
        if normal_images and self.auto_scale_images:
            scaled_images = []
            for img in normal_images:
                scaled_img = self._scale_image_to_fit(
                    img, self.rect.size, self.scale_func
                )
                scaled_images.append(scaled_img)
            normal_images = scaled_images

        # Ensure we have positions for all normal images (default to center if missing)
        while len(normal_positions) < len(normal_images):
            normal_positions.append((0.5, 0.5))

        # Check if normal images have changed
        if (
            normal_images != self.normal_images
            or normal_positions != self.normal_image_positions
        ):
            self.normal_images = normal_images
            self.normal_image_positions = normal_positions
            changed = True

        # Now process other states with fallback to normal
        other_state_mappings = [
            ("hovered", "hovered_images", "hovered_image_positions"),
            ("selected", "selected_images", "selected_image_positions"),
            ("disabled", "disabled_images", "disabled_image_positions"),
        ]

        for state_name, attr_name, position_attr_name in other_state_mappings:
            new_images = []
            new_positions = []

            # First try to load multi-image format (e.g., "hovered_images")
            try:
                image_details = self.ui_theme.get_image_details(
                    f"{state_name}_images", self.combined_element_ids
                )
                new_images = [detail["surface"] for detail in image_details]
                new_positions = [detail["position"] for detail in image_details]
            except LookupError:
                # Fall back to single image format (e.g., "hovered_image")
                try:
                    image_details = self.ui_theme.get_image_details(
                        f"{state_name}_image", self.combined_element_ids
                    )
                    if image_details:
                        new_images = [detail["surface"] for detail in image_details]
                        new_positions = [detail["position"] for detail in image_details]
                except LookupError:
                    # No image found for this state
                    pass

            # Apply auto-scaling if enabled
            if new_images and self.auto_scale_images:
                scaled_images = []
                for img in new_images:
                    scaled_img = self._scale_image_to_fit(
                        img, self.rect.size, self.scale_func
                    )
                    scaled_images.append(scaled_img)
                new_images = scaled_images

            # Handle fallbacks to normal state
            if not new_images:
                # Fall back to normal_images and normal_image_positions
                new_images = normal_images.copy()
                new_positions = normal_positions.copy()

            # Ensure we have positions for all images (default to center if missing)
            while len(new_positions) < len(new_images):
                new_positions.append((0.5, 0.5))

            # Check if images have changed
            current_images = getattr(self, attr_name)
            current_positions = getattr(self, position_attr_name, [])
            if new_images != current_images or new_positions != current_positions:
                setattr(self, attr_name, new_images)
                setattr(self, position_attr_name, new_positions)
                changed = True

        return changed


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


# overriding import
ui_manager.UIAppearanceTheme = UIAppearanceTheme


class UIManager(ui_manager.UIManager):
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
