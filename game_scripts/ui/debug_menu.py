from game_scripts.commander import get_commander
from game_scripts.tardigrade import Tardigrade
from game_scripts.thopter import Ornithopter
from scripts.camera import get_camera
from scripts.custom_sprites import AnimatedSprite, integer_scale
from scripts.ui_shim import UIButton
from scripts.tilemap import world_to_mapv
from game_scripts.game_tilemap import get_tilemap
from game_scripts.whiteboard import get_Whiteboard

from scripts.tilemap import TileData
import pygame as pg
from pygame.rect import Rect
from pygame_gui.elements import UIWindow


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
            object_id="#ornithopter_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning_state(Ornithopter),
        )
        UIButton(
            Rect(5, 56, 54, 46),
            "",
            object_id="#thopter_factory_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning_state(
                get_Whiteboard().tile_entities["thopter_factory_2"]
            ),
        )
        UIButton(
            Rect(64, 56, 54, 46),
            "",
            object_id="#sawmill_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning_state(
                get_Whiteboard().tile_entities["sawmill"]
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
        elif isinstance(self.spawning, TileData):
            self.spawn_tile()
            return
        # mouse pos ==camera.get_mouse_pos
        print("finally")
        pass

    def spawn_unit(self):
        entity = self.spawning
        entity(get_camera().get_global_mouse_pos())

    def spawn_tile(self):
        entity_to_spawn: TileData = self.spawning
        mouse_pos = get_camera().get_global_mouse_pos()
        map_pos = world_to_mapv(mouse_pos, entity_to_spawn.tile_size, True)
        entity_to_spawn.map_pos = map_pos
        new_tile = entity_to_spawn.tile_type(entity_to_spawn)
        if not get_tilemap().set_tile_in_map(
            new_tile, "active", entity_to_spawn.map_pos
        ):
            new_tile.kill()
        pass
