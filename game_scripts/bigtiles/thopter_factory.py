import pygame as pg

from game_scripts.bigtiles.bigtile import BigTile
from game_scripts.commander import get_commander
from game_scripts.group_server import get_group_server
from game_scripts.selectable import Selectable
from game_scripts.stockpile import get_stockpile
from game_scripts.ui.ui_elements import ContextPanel
from game_scripts.ui.ProgressPanel import ProgressPanel
from scripts.custom_sprites import integer_scale
from scripts.tilemap import TileData
from scripts.ui_shim import UIButton
from blinker import signal
from game_scripts.statistics import get_statistics


class ThopterFactory(BigTile, Selectable):
    def __init__(self, tiledata: TileData, *groups):
        super().__init__(
            tiledata,
            # get_group_server().colliders,
            get_group_server().update,  # prepending update to groups.
            *groups,
        )
        self.stop_construction()
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
                self.stop_construction()

    def get_construction_progress_fraction(self) -> float:
        # print(self.build_progress / get_statistics()["sawmill"]["build_time"])
        return (
            self.construction_progress
            / self.statistics[self.constructing]["build_time"]
        )

    def stop_construction(self):
        self.constructing = None
        self.construction_progress = 0.0

    def start_build_thopter(self):
        signal("start_build_thopter").send(self)
        self.constructing = "thopter"


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

        self.progress_panel = ProgressPanel(context_container, self.cancel_build)
        # BackgroundPanel(pg.Rect(120,-3,120,99),context_container)

    def start_build_thopter(self):
        factory: ThopterFactory = get_commander().first_selected
        factory.start_build_thopter()

    def cancel_build(self):
        factory: ThopterFactory = get_commander().first_selected
        factory.stop_construction()

    def update(self, _delta) -> None:
        if get_commander().first_selected.constructing:
            self.progress_panel.show()
            factory: ThopterFactory = get_commander().first_selected
            self.progress_panel.set_progress(
                factory.get_construction_progress_fraction() * 100
            )
        else:
            self.progress_panel.hide()
