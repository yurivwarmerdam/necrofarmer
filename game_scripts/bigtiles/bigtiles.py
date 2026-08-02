import pygame as pg
from pygame_gui.core import IContainerLikeInterface, ObjectID, UIElement
from pygame_gui.core.interfaces import IUIElementInterface
from pygame_gui.elements import UILabel, UIStatusBar

from game_scripts.bigtiles.bigtile import BigTile
from game_scripts.commander import get_commander
from game_scripts.group_server import get_group_server
from game_scripts.selectable import Selectable
from game_scripts.stockpile import get_stockpile
from game_scripts.ui.context_panel import ContextPanel
from scripts.custom_sprites import integer_scale
from scripts.tilemap import TileData
from scripts.ui_shim import UIButton
from blinker import signal
from game_scripts.statistics import get_statistics

from scripts.ui_shim import UIPanel
from scripts.custom_ui import ImagePanel
from functools import partial
from scripts.custom_sprites import ninepatchscale, tilingscale
from scripts.utils import load_image, sheet_to_sprite


class Sawmill(BigTile, Selectable):
    def __init__(self, tiledata: TileData, *groups):
        super().__init__(
            tiledata,
            # get_group_server().colliders,  # prepending colliders to groups.
            get_group_server().update,  # prepending update to groups.
            *groups,
        )
        self.saw_progress: float = 0
        self.stock = 0

    def update(self, _delta) -> None:
        if self.stock > 0:
            self.saw_progress += _delta / 1000
            if self.saw_progress >= 1:
                get_stockpile().add_wood(1)
                self.saw_progress = 0
                self.stock -= 1
        pass

    def put_wood(self, amount: int):
        self.stock += amount
        return amount

    def get_sawmill_progress(self):
        return self.saw_progress

    @property
    def context_panel(self) -> type[ContextPanel]:
        return SawmillPanel


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
            pg.Rect(0, 20, 100, 20),
            container=context_container,
            percent_method=get_commander().selected.sprites()[0].get_sawmill_progress,
        )

    def set_stock_text(self):
        self.stock_label.set_text(
            f"Logs: {str(get_commander().selected.sprites()[0].stock)}"
        )

    def update(self, _delta):
        if get_commander().selected.sprites()[0].stock == 0:
            self.progress_bar.visible = False
        else:
            self.progress_bar.visible = True
        self.set_stock_text()


class ThopterFactory(BigTile, Selectable):
    def __init__(self, tiledata: TileData, *groups):
        super().__init__(
            tiledata,
            # get_group_server().colliders,
            get_group_server().update,  # prepending update to groups.
            *groups,
        )
        self.stop_build()
        self.statistics = get_statistics()

    def put_wood(self, amount: int):
        get_stockpile().add_wood(amount)
        return amount

    @property
    def context_panel(self) -> type[ContextPanel]:
        return ThopterFactoryPanel

    def update(self, delta) -> None:
        if self.constructing:
            self.construction_progress += delta / 1000
            if (
                self.construction_progress
                >= self.statistics[self.constructing]["build_time"]
            ):
                match self.constructing:
                    case "thopter":
                        signal("spawn_thopter").send(self)
                    case x:
                        print(f"how are we here? {x}")
                self.stop_build()

    def start_build_thopter(self):
        signal("start_build_thopter").send(self)
        self.constructing = "thopter"

    def stop_build(self):
        self.constructing = None
        self.construction_progress = 0.0


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
            command=self.start_build_thopter,
        )
        self.cancel_button = UIButton(
            pg.Rect(56, 0, 54, 46),
            text="",
            object_id="#cancel_button",
            scale_func=integer_scale,
            container=context_container,
            command=self.cancel_build,
            visible=False,
        )

    def start_build_thopter(self):
        factory: ThopterFactory = get_commander().first_selected
        factory.start_build_thopter()

    def cancel_build(self):
        factory: ThopterFactory = get_commander().first_selected
        factory.stop_build()
        print("Should I be visible?")

    def update(self, _delta) -> None:
        if get_commander().first_selected.constructing:
            self.cancel_button.visible = True
        else:
            self.cancel_button.visible = False


class BackgroundPanel(UIPanel):
    def __init__(
        self,
        relative_rect: pg.Rect,
        container: IContainerLikeInterface | None = None,
        parent_element: UIElement | None = None,
        anchors: dict[str, str | IUIElementInterface] | None = {
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "top",
            },
        visible: int = 1,
    ):
        NINE_SLICE_FUNC = (
            partial(
                ninepatchscale,
                patch_margain=3,
                scale_func=tilingscale,
            ),
        )
        ui_components_sheet = load_image("art/ui_components.png")
        ui_background_sprite = sheet_to_sprite(
            ui_components_sheet, pg.Rect(0, 0, 60, 62)
        )
        super().__init__(
            relative_rect,
            container=container,
            parent_element=parent_element,
            anchors=anchors,
            visible=visible,
            scale_func=NINE_SLICE_FUNC,
        )
        self.context_background = ImagePanel(
            relative_rect,
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
            image_surf=ui_background_sprite,
            scale_func=NINE_SLICE_FUNC,
        )
