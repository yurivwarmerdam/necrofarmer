import pygame as pg
from typing import Dict
from pygame_gui.core import ObjectID, UIElement
from pygame_gui.core.interfaces import (
    IContainerLikeInterface,
    IUIElementInterface,
    IUIManagerInterface,
)
from pygame_gui.elements import UIImage, UIPanel
from pygame.rect import Rect, FRect
from scripts.custom_sprites import tilingscale, ninepatchscale
from scripts.utils import load_image, sheet_to_sprites, sheet_to_sprite
from functools import partial
from pygame import Vector2
from blinker import signal
from game_scripts.commander import Commander
from pygame.sprite import Group
import pygame_gui
from scripts.ui_shim import UIButton
import pygame

# This should be a container object; not a uipanel.
# Can definitely hold a bunch of utility functions.
class MainUI:
    def __init__(self):
        # setup main elements

        nine_slice_func = partial(
            ninepatchscale, patch_margain=3, scale_func=tilingscale
        )
        portrait_panel_rect: Rect = Rect(0, 0, 170, 146)
        context_panel_rect: Rect = Rect(0, 0, 400, 99)
        ui_components_sheet = load_image("art/ui_components.png")
        portrait_background_sprite = sheet_to_sprite(
            ui_components_sheet, Rect(0, 112, 170, 146)
        )
        ui_background_sprite = sheet_to_sprite(ui_components_sheet, Rect(0, 0, 60, 62))

        # ------- base elements -------

        portrait_panel = UIPanel(
            pg.Rect(
                0,
                -portrait_panel_rect[3],
                portrait_panel_rect[2],
                portrait_panel_rect[3],
            ),
            anchors={
                "left": "left",
                "right": "left",
                "top": "bottom",
                "bottom": "bottom",
            },
            object_id="#portrait_background"
        )
        # portrait_background = UIImage(
        #     portrait_panel_rect,
        #     portrait_background_sprite,
        #     anchors={
        #         "left": "left",
        #         "right": "right",
        #         "top": "top",
        #         "bottom": "bottom",
        #     },
        #     container=portrait_panel.get_container(),
        # )
        # print(portrait_panel.rect)

        context_panel = UIPanel(
            pg.Rect(
                portrait_panel_rect[2]-2,
                -(context_panel_rect[3]-1),
                context_panel_rect[2],
                context_panel_rect[3],
            ),
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            }
        )
        context_background = UIImage(
            context_panel_rect,
            ui_background_sprite,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
            scale_func=nine_slice_func,
            container=context_panel.get_container()
        )

        # buttons to be moved to context:

        portrait_button = UIButton(
            pg.Rect(3, 3, 54 * 3, 46 * 3),
            text="",
            object_id="#thopter_button",
            scale_func=pygame.transform.scale,
            container=portrait_panel.get_container(),
        )

        image_button = UIButton(
            pg.Rect(3, 3, 54, 46),
            text="",
            object_id="#thopter_button",
            container=context_panel.get_container(),
        )

        # signals we are observing
        selected_changed = signal("selected_changed")
        selected_changed.connect(self.selected_changed)

    def selected_changed(self, sender: Commander, **kwargs):
        # create appropriate contextpanel, depending on what is selected
        print(f"changing selected. Sender: {sender}")
        for i in sender.selected:
            print(type(i))


# This should be passed portrait panel and context panel. Portrait gives either big image, or a series of small thumbs.
# context is contextual, based on what's selected.
class ContextPanel(UIPanel):
    def __init__(
        self,
        relative_rect: Rect | FRect | tuple[float, float, float, float],
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
        )

    pass
