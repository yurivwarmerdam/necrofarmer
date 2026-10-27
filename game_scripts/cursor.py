from pygame import Rect, Surface
from pygame.math import Vector2
from pygame.sprite import Sprite

from scripts.tilemap.tmx_parser import get_tmx_parser
from scripts.camera import get_camera
from scripts.custom_sprites import NodeSprite
from scripts.group_server import get_group_server
from scripts.utils import sheet_to_sprite


class Cursor(NodeSprite):
    def __init__(self):
        super().__init__(
            sheet_to_sprite("art/sprites_1_1.png", Rect(45, 35, 14, 10)),
            Vector2(100, 100),
            "center",
            Vector2(0, 0),
            get_group_server().front,
            get_group_server().update,
        )
        self.build_surf: Surface | None = None
        self.active_building = ""

    def update(self, _delta):
        self.pos = get_camera().get_global_mouse_pos()
        if self.build_surf:
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
        self.build_surf = get_tmx_parser().named_data[build_name].surf
        print(self.build_surf.get_rect())
        # perhaps surf.copy
        # I am a sprite. make this my surf.
        # do math for rects, I guess

        # also look up the corresponding sprite in tilemap, put that in some var,
        # maybe make it own sprite?

    def disable_build(self):
        self.build_surf = None
        self.active_building = ""
