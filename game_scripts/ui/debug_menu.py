import pygame as pg
from pygame.rect import Rect
from pygame_gui.elements import UIWindow

from game_scripts.commander import get_commander
from game_scripts.game_tilemap import get_tilemap
from game_scripts.tardigrade import Tardigrade
from game_scripts.thopter import Thopter
from scripts.camera import get_camera
from scripts.custom_sprites import AnimatedSprite, integer_scale
from scripts.tilemap import TileData, world_to_mapv
from scripts.ui_shim import UIButton


class DebugMenu(UIWindow):
    def __init__(self) -> None:
        super().__init__(Rect(510, 30, 125, 200), resizable=True)
        get_commander().debug = self
        self.spawning: type[AnimatedSprite] | TileData | None = None

        UIButton(
            Rect(5, 5, 54, 46),
            "",
            object_id="#tardigrade_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning_state(Tardigrade),
        )
        UIButton(
            Rect(64, 5, 54, 46),
            "",
            object_id="#thopter_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning_state(Thopter),
        )
        UIButton(
            Rect(5, 56, 54, 46),
            "",
            object_id="#thopter_factory_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning_state(
                "thopter_factory_2"
            ),
        )
        UIButton(
            Rect(64, 56, 54, 46),
            "",
            object_id="#sawmill_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning_state(
                "sawmill"
            ),
        )

    def set_spawning_state(self, sprite_type: type[AnimatedSprite] | TileData):
        self.spawning = sprite_type

    def process_events(self, event: pg.event.Event) -> bool:
        if not self.spawning:
            return False
        if event.type == pg.MOUSEBUTTONUP:
            if event.button != 1:
                self.spawning = None
                return False
            self.do_spawn()
            return True
        return False

    def do_spawn(self) -> None:
        if isinstance(self.spawning, type):
            if issubclass(self.spawning, AnimatedSprite):
                self.spawn_unit()
                return
        elif isinstance(self.spawning, str):
            self.spawn_tile()
            return
        print("finally")
        pass

    def spawn_unit(self):
        entity = self.spawning
        entity(get_camera().get_global_mouse_pos())

    def spawn_tile(self):
        get_tilemap().spawn_tile_str(self.spawning,get_camera().get_global_mouse_pos(),"active")
