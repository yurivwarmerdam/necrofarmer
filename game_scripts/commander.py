import pygame as pg

class Commander():
    def __init__(self):
        self.selected=None

    def process_events(self, event:pg.event.Event)->bool:
        is_processed = False
        if self.selected:
            pass

        # right click:
        # if selected:
        #
        # left click:
        # find everything in the selectable Group
        #   if any: select()
        #
        return is_processed