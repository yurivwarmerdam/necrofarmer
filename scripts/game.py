from abc import ABC

import pygame as pg


class Game(ABC):
    def __init__(self) -> None:
        self.clock = pg.time.Clock()

        pass

    def run(self):
        while True:
            _delta = self.clock.get_time()
            self.process_events()
            self.update()

    def process_events(self):
        # event loop
        pass

    def update(self):
        # update whatever needs update running
        pass
