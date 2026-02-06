from pygame import Vector2
from game_scripts.entity_tilemap import BigTile
from game_scripts.selectable import Selectable
from scripts import group_server
from game_scripts.game_ui import ContextPanel
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
        groups = global_groups.colliders + groups
        super().__init__(
            pos, image, properties, *groups, anchor=anchor, offset=offset, tiles=tiles
        )

        @property
        def context_panel(self) -> type[ContextPanel]:
            return SawmillPanel


class SawmillPanel(ContextPanel):
    def __init__(self) -> None:
        self._portrait_button = UIButton(
            pg.Rect(3, 3, 54 * 3, 46 * 3),
            text="",
            # object_id="#thopter_button",
            scale_func=integer_scale,
            # container=main_ui.portrait_panel.get_container(),
        )
        self._image_button = UIButton(
            pg.Rect(3, 3, 54, 46),
            text="",
            # object_id="#thopter_button",
            scale_func=integer_scale,
            # container=main_ui.context_panel.get_container(),
        )
        super().__init__("#sawmill_button")
        pass

    @property
    def portrait_button(self) -> UIButton:
        return self.portrait_button
        raise NotImplementedError

    @property
    def image_button(self) -> UIButton:
        raise NotImplementedError
