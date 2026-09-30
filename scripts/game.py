from abc import ABC, abstractmethod

import pygame as pg

class Game(ABC):
    # params editable (in config file?)
    def __init__(self,resolution:tuple[int,int]) -> None:
        pg.init()

        self.display = pg.display.set_mode(
        resolution,
        pg.RESIZABLE,
        # pg.SCALED,
        )
        #editable theme path(s)
        self.ui_manager = pygame_gui.UIManager(resolution, theme_path="theme/theme.json")
        self.ui_manager.get_theme().load_theme("theme/buttons_generated.json")
        self.clock = pg.time.Clock()

        # late init (after group server made groups in game-specific inits)
        # alternatively: have camera know group server, which is engine-specific now anyway
        # the second allows up to dynamically change render groups during runtime
        camera = initialize_camera(
        group_server.render_groups,
        Group(),
        display,
        Vector2(-300, 0),
        )

        pass

    def run(self):
        while True:
            delta = self.clock.get_time()
            events = pg.event.get()
            self.process_events(events)
            self.update(delta)

    @abstractmethod
    def process_events(self,events):
        # event loop
        pass

    @abstractmethod
    def update(self,delta):
        # update whatever needs update running
        pass
