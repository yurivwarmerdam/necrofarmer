from typing import Any

from pygame.sprite import Group, Sprite


class Cursor(Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self.active_building = ""

    def update(self, *args: Any, **kwargs: Any) -> None:
        # set pos(center?) to mouse global cursor pos
        # if constructing: grab building sprite (might do that when initializing building):
        #   quantize building pos to tilemap
        #   if can build:
        #       set color to regular, but less opaque
        #   else:
        #       set color to be more red (reduce g and b)
        pass

    def enable_build(self, build_name: str):
        self.active_building = build_name
        # also look up the corresponding sprite in tilemap, put that in some var,
        # maybe make it own sprite?

    def disable_build(self):
        self.active_building = ""
