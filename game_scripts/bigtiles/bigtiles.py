from typing import Any

import pygame as pg

from game_scripts.group_server import get_group_server
from game_scripts.bigtiles.bigtile import BigTile
from game_scripts.ui.context_panel import ContextPanel
from game_scripts.selectable import Selectable
from scripts.custom_sprites import integer_scale
from scripts.ui_shim import UIButton
from scripts.tilemap import TileData
from pygame_gui.elements import UILabel, UIStatusBar
from game_scripts.stockpile import get_stockpile


class Sawmill(BigTile, Selectable):
    def __init__(self, tiledata: TileData, *groups):
        super().__init__(
            tiledata,
            get_group_server().colliders,  # prepending colliders to groups.
            get_group_server().update,
            *groups,
        )
        self.stock = 1000

    @property
    def context_panel(self) -> type[ContextPanel]:
        return SawmillPanel

    def update(self, _delta) -> None:
        if self.stock > 0:
            get_stockpile().add_wood(1)
            self.stock -= 1
        pass


class SawmillPanel(ContextPanel):
    def __init__(self, context_container) -> None:
        super().__init__(
            portrait_id="#sawmill_button",
            context_container=context_container,
        )

        self.stock_label = UILabel(
            pg.Rect(0, 0, 100, 16),
            "",
            container=context_container,
        )
        self.set_stock_text()

        self.progress_bar = UIStatusBar(
            pg.Rect(0, 50, 100, 20),
            container=context_container,
        )

    def set_stock_text(self):
        self.stock_label.set_text(
            f"Logs: {str(self.commander.selected.sprites()[0].stock)}"
        )

    def update(self, _delta):
        if self.commander.selected.sprites()[0].stock == 0:
            self.progress_bar.visible = False
        else:
            self.progress_bar.visible = True
        self.set_stock_text()


class ThopterFactory(BigTile, Selectable):
    def __init__(self, tiledata: TileData, *groups):
        super().__init__(
            tiledata,
            get_group_server().colliders,  # prepending colliders to groups.
            get_group_server().update,
            *groups,
        )

    @property
    def context_panel(self) -> type[ContextPanel]:
        return ThopterFactoryPanel


class ThopterFactoryPanel(ContextPanel):
    def __init__(self, context_container) -> None:
        super().__init__(
            portrait_id="#thopter_factory_2_button",
            context_container=context_container,
        )
        UIButton(
            pg.Rect(0, 0, 54, 46),
            text="",
            object_id="#thopter_button",
            scale_func=integer_scale,
            container=context_container,
            command=lambda: print("I do nothing yet!"),
        )
