from functools import partial

import pygame as pg
from blinker import signal
from pygame.rect import Rect
from pygame_gui.elements import UIImage

from game_scripts.commander import Commander
from game_scripts.context_panel import ContextPanel
from scripts.custom_sprites import integer_scale, ninepatchscale, tilingscale
from scripts.ui_shim import UIButton, UIPanel
from scripts.utils import load_image, sheet_to_sprite


class MainUI:
    """
    This should be a container object; not the actual panel.
    Can definitely hold a bunch of utility functions.
    """

    def __init__(self):
        # setup main elements

        nine_slice_func = partial(
            ninepatchscale, patch_margain=3, scale_func=tilingscale
        )
        portrait_panel_rect: Rect = Rect(0, 0, 170, 146)
        context_panel_rect: Rect = Rect(0, 0, 400, 99)
        ui_components_sheet = load_image("art/ui_components.png")
        ui_background_sprite = sheet_to_sprite(ui_components_sheet, Rect(0, 0, 60, 62))

        # ------- base elements -------

        self.active_panel = None
        # TODO: Be more consistent here.
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

        self.context_background = UIPanel(
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
            # object_id="#panel_background",
            scale_func=nine_slice_func,
        )
        UIImage(
            context_panel_rect,
            ui_background_sprite,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
            scale_func=nine_slice_func,
            container=self.context_background.get_container(),
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
            self.set_context_panel(sender)
            UIButton(
                Rect(4, 4, 54 * 3, 46 * 3),
                text="",
                object_id=self.active_panel.portrait_id,
                scale_func=integer_scale,
                container=self.portrait_panel,
                command=lambda: sender.unselect(sender.selected.sprites()[0]),
            )

    def set_context_panel(self, commander: Commander):
        new_panel: type[ContextPanel] = commander.selected.sprites()[0].context_panel
        self.active_panel = new_panel(commander=commander)
        self.active_panel.set_context_elems(self.context_panel.get_container())
        pass

    def update(self,_delta):
        if self.active_panel:
            self.active_panel.update(_delta)