from pygame import Rect, Surface
from pygame.math import Vector2
from pygame.sprite import Sprite

from scripts.tilemap.tmx_parser import get_tmx_parser
from scripts.camera import get_camera
from scripts.custom_sprites import NodeSprite
from scripts.group_server import get_group_server
from scripts.utils import sheet_to_sprite
from scripts.tilemap import tilemap_utils


class Cursor(NodeSprite):
    def __init__(self):
        self.cursor_image = sheet_to_sprite("art/sprites_1_1.png", Rect(45, 35, 14, 10))
        # self.cursor_image = cursor_image.copy()
        super().__init__(
            self.cursor_image,
            Vector2(100, 100),
            "center",
            Vector2(0, 0),
            get_group_server().front,
            get_group_server().update,
        )
        # self.build_surf: Surface | None = None
        self.tile_size = Vector2()
        self.active_building = ""

    def update(self, _delta):
        new_pos = get_camera().get_global_mouse_pos()
        if self.tile_size:
            tl = tilemap_utils.world_to_mapv(new_pos, self.tile_size, True)
            snapped_pos = tilemap_utils.map_to_worldv(tl, self.tile_size, True)
            new_pos = snapped_pos

        self.pos = new_pos
        # if constructing: grab building sprite (might do that when initializing building):
        #   quantize building pos to tilemap
        #   if can build:
        #       set color to regular, but less opaque
        #   else:
        #       set color to be more red (reduce g and b)
        pass

    def enable_build_plan(self, build_name: str):
        self.active_building = build_name
        tiledata = get_tmx_parser().named_data[build_name]
        surf = tiledata.surf
        offset = tiledata.offset
        self.rect = surf.get_rect()
        self.offset = offset
        self.anchor = tiledata.anchor
        self.image = surf
        self.tile_size = tiledata.tile_size
        surf.set_alpha(170)

    def disable_build_plan(self):
        print("disabling")
        self.active_building = ""
        self.rect = self.cursor_image.get_rect()
        self.image = self.cursor_image
        self.offset = Vector2()
        self.anchor = "center"
        self.tile_size = Vector2()

    def is_build_planning(self):
        return bool(self.active_building)
