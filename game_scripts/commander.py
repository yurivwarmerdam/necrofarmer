import pygame as pg
from pygame.sprite import Sprite


class SelectBox(Sprite):
    pass

class Commander():
    """
    Keeps track of any selected units.
    Defers inputs to 
    """
    def __init__(self):
        self.selected=None
        self.dragging=False

    def process_events(self, event:pg.event.Event)->bool:
        is_processed = False
        if self.selected:
            is_processed = self.selected.process_events(event)
        elif event is pg.MOUSEBUTTONDOWN:
            #rect stuff with dragging

        # right click:
        # if selected:
        #
        # left click:
        # find everything in the selectable Group
        #   if any: select()
        #
        return is_processed