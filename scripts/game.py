from abc import ABC, abstractmethod
import sys

import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Group
import pygame_gui

from scripts.camera import initialize_camera
from scripts.image_server import get_image_server


class Game(ABC):
    # params editable (in config file?)
    def __init__(self, resolution: tuple[int, int]) -> None:
        pg.init()

        self.display = pg.display.set_mode(
            resolution,
            pg.RESIZABLE,
            # pg.SCALED,
        )
        # editable theme path(s)
        self.ui_manager = pygame_gui.UIManager(
            resolution, theme_path="theme/theme.json"
        )
        self.ui_manager.get_theme().load_theme("theme/buttons_generated.json")
        self.clock = pg.time.Clock()

        # late init (after group server made groups in game-specific inits)
        # alternatively: have camera know group server, which is engine-specific now anyway
        # the second allows up to dynamically change render groups during runtime
        self.camera = initialize_camera(
            self.display,
            Vector2(-300, 0),
        )

        img_server = get_image_server()

        pass

    def main(self):
        while True:
            delta = self.clock.get_time()
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
                    pg.quit()
                    sys.exit()
            self.process_events(events)
            self.update(delta)
            # render stuff
            self.camera.draw_all()
            pg.display.update()
            self.clock.tick(60)


    @abstractmethod
    def process_events(self, events):
        # event loop
        pass

    def update(self, delta):
        self.group_server.draw.update()
        self.group_server.update.update(delta)
        self.ui.update(delta)
        self.ui_manager.update(delta / 1000)
