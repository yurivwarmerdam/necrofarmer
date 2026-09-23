from scripts.custom_sprites import NodeSprite
from game_scripts.group_server import get_group_server
from scripts.utils import sheet_to_sprite
from pygame import Rect
from pygame.math import Vector2
from scripts.camera import get_camera
from game_scripts.game_tilemap import get_tilemap


class Cursor(NodeSprite):
    def __init__(self):
        super().__init__(
            sheet_to_sprite("art/sprites_1_1.png", Rect(45, 35, 14, 10)),
            Vector2(100, 100),
            "center",
            Vector2(0, 0),
            get_group_server().render_groups["front"],
            get_group_server().update,
        )
        self.active_building = ""

    def update(self, _delta):
        self.pos = get_camera().get_global_mouse_pos()
        if self.active_building:
            pass
        # if constructing: grab building sprite (might do that when initializing building):
        #   quantize building pos to tilemap
        #   if can build:
        #       set color to regular, but less opaque
        #   else:
        #       set color to be more red (reduce g and b)
        pass

    def enable_build(self, build_name: str):
        self.active_building = build_name
        get_tilemap().named_tiledata[build_name]
        # also look up the corresponding sprite in tilemap, put that in some var,
        # maybe make it own sprite?

    def disable_build(self):
        self.active_building = ""
