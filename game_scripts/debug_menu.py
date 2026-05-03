from game_scripts.commander import get_commander
from game_scripts.tardigrade import Tardigrade
from game_scripts.thopter import Ornithopter
from scripts.camera import get_camera
from scripts.custom_sprites import AnimatedSprite, integer_scale
from scripts.ui_shim import UIButton


import pygame as pg
from pygame.rect import Rect
from pygame_gui.elements import UIWindow


class DebugMenu(UIWindow):
    def __init__(self) -> None:
        super().__init__(Rect(510, 30, 125, 200), resizable=True)
        get_commander().special = self
        self.spawning: type[AnimatedSprite] | None = None

        UIButton(
            Rect(5, 5, 54, 46),
            "",
            object_id="#tardigrade_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning(Tardigrade),
        )
        UIButton(
            Rect(64, 5, 54, 46),
            "",
            object_id="#ornithopter_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: self.set_spawning(Ornithopter),
        )
        UIButton(
            Rect(5, 56, 54, 46),
            "",
            object_id="#thopter_factory_button",
            scale_func=integer_scale,
            container=self,
            command=lambda: print("draw owl here"),
        )

    def set_spawning(self, sprite_type: type[AnimatedSprite]):
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

        # if event is inputeventmousebutton and event is left click and event is button up:
        # do_spawn(self.spawning)
        # if event is right click up:
        # self.spawning =None

    def do_spawn(self) -> None:
        # mouse pos ==camera.get_mouse_pos
        type = self.spawning
        type(get_camera().get_global_mouse_pos())
        pass