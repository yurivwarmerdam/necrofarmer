import pygame as pg
from pygame import Vector2, Rect
from pygame.sprite import Sprite
from dataclasses import dataclass
from scripts.camera import Camera, get_camera


@dataclass
class SelectBox:
    start: Vector2 | None = None
    rect = Rect(0, 0, 0, 0)

    def set_start(self):
        self.camera = get_camera()
        self.start = self.camera.get_global_mouse_pos()

    @property
    def dragging(self) -> bool:
        if not self.start:
            return False
        travel: Vector2 = self.start - self.camera.get_global_mouse_pos()
        return travel.length() > 0

    def draw(self, surface):
        if self.dragging and self.start:
            mo = self.camera.get_global_mouse_pos()
            tl = Vector2(min((self.start.x, mo[0])), min((self.start.y, mo[1]))) - self.camera.pos
            br = Vector2(max((self.start.x, mo[0])), max((self.start.y, mo[1]))) - self.camera.pos
            self.rect.update(tl, br)
            # Could potentially be replaced by surface.fill() in the future.
            pg.draw.rect(surface, "darkgreen", self.rect, 1)

    def get_intersects(self):
        pass


class Commander:
    """
    Keeps track of any selected units.
    Defers inputs to
    """

    def __init__(self):
        self.selected = []
        self.dragging = False
        self.select_box = SelectBox()
        self.camera = get_camera()

    def process_events(self, event: pg.event.Event) -> bool:
        is_processed = False
        if self.selected:
            is_processed = self.selected.process_events(event)
        if not is_processed:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.select_box.set_start()
                is_processed = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.select_box.dragging:
                    self.select_box.start = None
                    # do box select
                else:
                    self.camera.get_global_mouse_pos()
                    # use that to check for overlaps
                    # unselect/select based on rules

        # right click:
        # if selected:
        #
        # left click:
        # find everything in the selectable Group
        #   if any: select()
        #
        return is_processed
