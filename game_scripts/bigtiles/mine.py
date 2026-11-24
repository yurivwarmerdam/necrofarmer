from pygame import Rect
from blinker import signal
from pygame_gui.elements import UIWindow

from game_scripts.bigtiles.bigtile import BigTile
from game_scripts.commander import get_commander
from game_scripts.selectable import Selectable
from game_scripts.statistics import get_statistics
from game_scripts.stockpile import get_stockpile
from game_scripts.ui.ProgressPanel import ProgressPanel
from game_scripts.ui.ui_elements import ContextPanel
from scripts.custom_sprites import integer_scale
from scripts.tilemap.tilemap import TileData
from scripts.ui_shim import UIButton


class Mine(BigTile, Selectable):
    def __init__(self, tiledata: TileData):
        super().__init__(tiledata)
        self.statistics = get_statistics()
        self.mineshaft

    def put_wood(self, amount: int):
        get_stockpile().add_wood(amount)
        return amount

    @property
    def context_panel(self) -> type[ContextPanel]:
        return MinePanel

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
        return (
            self.construction_progress
            / self.statistics[self.constructing]["build_time"]
        )


class MinePanel(ContextPanel):
    def __init__(self, context_container) -> None:
        super().__init__(
            portrait_id="#mine_button",
            context_container=context_container,
        )
        UIButton(
            Rect(5, 5, 54, 46),
            "into the pit",
            object_id="#tardigrade_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: MinePopup(),
        )
        # gem amounts, occupied by tardigrade status, other stuff?

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


class MinePopup(UIWindow):
    pass
