import pygame as pg
from pygame import Vector2, Rect
from pygame.sprite import Sprite
from dataclasses import dataclass
from scripts.camera import Camera, get_camera

camera=get_camera()

@dataclass
class SelectBox():
    start:Vector2 | None=None
    rect=Rect(0,0,0,0)

    def set_start(self):
        self.start=camera.get_global_mouse_pos()

    @property
    def dragging(self)->bool:
        if not self.start:
            return False
        travel:Vector2 = self.start - camera.get_global_mouse_pos()
        return travel.length() > 0

    def draw(self,surface):
        if self.dragging and self.start:
            mo = pg.mouse.get_pos()
            tl = Vector2(min((self.start.x, mo.x)),min((self.start.y, mo.y)))
            br = Vector2(max((self.start.x, mo.x)),max((self.start.y, mo.y)))
            self.rect.update(tl,br)
            pg.draw.rect(surface, "darkgreen",self.rect,1)
            

    def get_intersects(self):
        pass


class Commander():
    """
    Keeps track of any selected units.
    Defers inputs to 
    """
    def __init__(self):
        self.selected=[]
        self.dragging=False
        self.select_box=SelectBox()

    def process_events(self, event:pg.event.Event)->bool:
        is_processed = False
        if self.selected:
            is_processed = self.selected.process_events(event)
        elif event is pg.MOUSEBUTTONDOWN:
            self.select_box.set_start()
        elif event is pg.MOUSEBUTTONUP:
            if self.select_box.dragging:
                #do box select
            else:
                camera.get_global_mouse_pos()
                # use that to check for overlaps

        # right click:
        # if selected:
        #
        # left click:
        # find everything in the selectable Group
        #   if any: select()
        #
        return is_processed