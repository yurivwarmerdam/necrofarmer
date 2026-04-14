import pygame as pg
from pygame import Vector2

from game_scripts import group_server
from game_scripts.bigtiles.bigtile import BigTile
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
    def __init__(self, context_container) -> None:
        super().__init__(
            portrait_id="#sawmill_button",
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


class ThopterFactory(BigTile, Selectable):
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
