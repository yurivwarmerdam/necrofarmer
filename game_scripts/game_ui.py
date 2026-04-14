from functools import partial
from typing import Any, Dict


import pygame as pg
from pygame.transform import smoothscale
import pygame_gui
from blinker import signal
from pygame.rect import Rect
from pygame_gui.core import IContainerLikeInterface, ObjectID, UIElement
from pygame_gui.core.interfaces import IUIElementInterface, IUIManagerInterface
from pygame_gui.elements import UIWindow

from game_scripts.commander import Commander,get_commander
from game_scripts.context_panel import ContextPanel
from scripts.custom_sprites import integer_scale, ninepatchscale, tilingscale
from scripts.ui_shim import UIButton, UIPanel
from pygame_gui.elements import UIPanel as UIPanel_original
from scripts.utils import load_image, sheet_to_sprite
from pygame_gui.core.utility import get_default_manager
from scripts.custom_ui import NINE_SLICE_FUNC, ImagePanel


class MainUI:
    """
    This should be a container object; not the actual panel.
    Can definitely hold a bunch of utility functions.
    """

    def __init__(self):
        # setup main elements

        # nine_slice_func = partial(
        #     ninepatchscale, patch_margain=3, scale_func=tilingscale
        # )
        portrait_panel_rect: Rect = Rect(0, 0, 170, 146)
        context_panel_rect: Rect = Rect(0, 0, 400, 99)
        ui_components_sheet = load_image("art/ui_components.png")
        self.ui_background_sprite = sheet_to_sprite(
            ui_components_sheet, Rect(0, 0, 60, 62)
        )

        self.main_menu = None

        # ------- base elements -------

        self.active_panel = None

        self.menu_button = UIButton(
            pg.Rect(-126, 0, 126, 18),
            "Menu",
            anchors={
                "left": "right",
                "right": "right",
                "top": "top",
                "bottom": "top",
            },
            object_id="#menu_button",
            command=self.toggle_main_menu,
        )

        self.portrait_panel = UIPanel(
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
            object_id="#portrait_background",
        )

        self.context_background = ImagePanel(
            pg.Rect(
                portrait_panel_rect[2],
                -(context_panel_rect[3]),
                context_panel_rect[2],
                context_panel_rect[3],
            ),
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
            image_surf=self.ui_background_sprite,
            scale_func=NINE_SLICE_FUNC,
        )

        self.context_panel = UIPanel(
            Rect(
                portrait_panel_rect[2] + 3,
                -(context_panel_rect[3]) + 3,
                context_panel_rect[2] - 6,
                context_panel_rect[3] - 6,
            ),
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
        )

        # signals we are observing
        selected_changed = signal("selected_changed")
        selected_changed.connect(self.selected_changed, weak=False)

    def selected_changed(self, sender: Commander):
        """
        create appropriate contextpanel, depending on what is selected
        """
        if self.active_panel:
            self.active_panel = None
            self.portrait_panel.get_container().clear()
            self.context_panel.get_container().clear()
        if sender.selected:
            self.set_context_panel()
            UIButton(
                Rect(4, 4, 54 * 3, 46 * 3),
                text="",
                object_id=self.active_panel.portrait_id,
                scale_func=integer_scale,
                container=self.portrait_panel,
                command=lambda: sender.unselect(sender.selected.sprites()[0]),
            )

    def toggle_main_menu(self):
        if self.main_menu:
            self.main_menu.kill()
            self.main_menu = None
        else:
            self.main_menu = MainMenu()

    def set_context_panel(self):
        new_panel: type[ContextPanel] = get_commander().selected.sprites()[0].context_panel
        self.active_panel = new_panel(
            context_container=self.context_panel.get_container()
        )

    def update(self, _delta):
        if self.active_panel:
            self.active_panel.update(_delta)


class MainMenu(ImagePanel):
    def __init__(self):
        ui_components_sheet = load_image("art/ui_components.png")
        ui_background_sprite = sheet_to_sprite(ui_components_sheet, Rect(0, 0, 60, 62))
        super().__init__(
            Rect(0, 0, 150, 100),
            anchors={
                "center": "center",
            },
            image_surf=ui_background_sprite,
            scale_func=NINE_SLICE_FUNC,
        )
        UIButton(
            pg.Rect(0, 10, 126, 18),
            "Debug Menu",
            anchors={"centerx": "centerx", "top": "top"},
            object_id="#menu_button",
            container=self.get_container(),
            command=self.toggle_debug_window,
        )

    def toggle_debug_window(self):
        for elem in self.ui_manager.get_root_container().elements:
            if isinstance(elem, DebugMenu):
                elem.kill()
                return
        DebugMenu()


class DebugMenu(UIWindow):
    def __init__(self) -> None:
        super().__init__(Rect(30, 30, 125, 100))

        UIButton(
            Rect(5, 5, 54, 46),
            "",
            object_id="#tardigrade_button",
            scale_func=integer_scale,
            container=self,
        )
        UIButton(
            Rect(64, 5, 54, 46),
            "",
            object_id="#ornithopter_button",
            scale_func=integer_scale,
            container=self,
        )
