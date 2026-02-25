import pygame as pg
from pygame import Vector2

from game_scripts import group_server
from game_scripts.big_tile import BigTile
from game_scripts.game_ui import ContextPanel
from game_scripts.selectable import Selectable
from scripts.custom_sprites import integer_scale
from scripts.ui_shim import UIButton


class Sawmill(BigTile, Selectable):
    def __init__(
        self,
        pos,
        image,
        properties: dict,
        *groups,
        anchor="bottomleft",
        offset=Vector2(0, 0),
        tiles: list = [Vector2(0, 0)],
    ):
        global_groups = group_server.get_server()
        super().__init__(
            pos,
            image,
            properties,
            global_groups.colliders,  # prepending colliders to groups.
            *groups,
            anchor=anchor,
            offset=offset,
            tiles=tiles,
        )

    @property
    def context_panel(self) -> type[ContextPanel]:
        return SawmillPanel


class SawmillPanel(ContextPanel):
    def __init__(self) -> None:
        super().__init__("#sawmill_button")

    @property
    def image_button(self) -> UIButton:
        return UIButton(
            pg.Rect(3, 3, 54, 46),
            text="",
            # object_id="#thopter_button",
            scale_func=integer_scale,
            # container=main_ui.context_panel.get_container(),
        )

    @property
    def context_panel(self):
        raise NotImplementedError
