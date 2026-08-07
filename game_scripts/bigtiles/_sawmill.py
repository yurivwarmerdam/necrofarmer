from typing import Any
from game_scripts.commander import get_commander
from game_scripts.bigtiles.bigtile import BigTile
from game_scripts.selectable import Selectable
from game_scripts.ui.ui_elements import ContextPanel
from scripts.tilemap import TileData
from game_scripts.group_server import get_group_server
from game_scripts.ui.ProgressPanel import ProgressPanel
from game_scripts.statistics import get_statistics

class _Sawmill(BigTile, Selectable):
    def __init__(self, tiledata: TileData, *groups):
        super().__init__(
            tiledata,
            get_group_server().update,  # prepending update to groups.
            *groups,
        )
        self.build_progress = 0.0

    def get_construction_progress_fraction(self):
        return self.build_progress / get_statistics()["sawmill"]["build_time"]

    def construct(self, amount):
        self.build_progress = min(
            self.build_progress + amount, get_statistics()["sawmill"]["build_time"]
        )
        if self.get_construction_progress_fraction() >= 1:
            self.jobs_done()

    def jobs_done(self):
        # spawn replacement
        if self in get_commander().selected.sprites():
            # get_commander().select(newly spawned replacement)
            pass
        get_commander().unselect(self)
        self.kill()

    # currently only doing update for debugging purposes.
    def update(self, _delta) -> None:
        self.construct(_delta / 1000)

    def stop_construction(self):
        # Let's see how easy this is.
        get_commander().unselect(self)
        self.kill()

    @property
    def context_panel(self) -> type[ContextPanel]:
        return _SawmillPanel


class _SawmillPanel(ContextPanel):
    def __init__(self, context_container) -> None:
        super().__init__(
            portrait_id="#_sawmill_button",
            context_container=context_container,
        )
        self.progress_panel: ProgressPanel = ProgressPanel(
            context_container, self.cancel_build
        )

    def cancel_build(self):
        mill: _Sawmill = get_commander().first_selected
        mill.stop_construction()

    def update(self, _delta) -> None:
        mill: _Sawmill = get_commander().first_selected
        self.progress_panel.set_progress(
            mill.get_construction_progress_fraction() * 100
        )
