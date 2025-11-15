import pygame as pg
from pygame import Vector2, Rect, Surface
from pygame.sprite import Sprite
from dataclasses import dataclass
from scripts.camera import Camera, get_camera
from scripts.custom_sprites import NodeSprite


# @dataclass
# class SelectBox:
#     start: Vector2 | None = None
#     rect = Rect(0, 0, 0, 0)

#     def set_start(self):
#         self.camera = get_camera()
#         self.start = self.camera.get_global_mouse_pos()

#     @property
#     def dragging(self) -> bool:
#         if not self.start:
#             return False
#         travel: Vector2 = self.start - self.camera.get_global_mouse_pos()
#         return travel.length() > 0

#     def draw(self, surface):
#         if self.dragging and self.start:
#             mo = self.camera.get_global_mouse_pos()
#             tl = Vector2(min((self.start.x, mo[0])), min((self.start.y, mo[1]))) - self.camera.pos
#             br = Vector2(max((self.start.x, mo[0])), max((self.start.y, mo[1]))) - self.camera.pos
#             self.rect.update(tl, br)
#             # Could potentially be replaced by surface.fill() in the future.
#             pg.draw.rect(surface, "darkgreen", self.rect, 1)

#     def get_intersects(self):
#         pass


class SelectBox(NodeSprite):
    def __init__(self) -> None:
        super().__init__(Surface((0, 0)))
        self.color = pg.Color(34, 135, 34)
        self.image.fill(self.color)
        self.image.set_alpha(128)
        self.dragging: bool = False
        self.start = Vector2()
        self.camera = get_camera()

    def start_drag(self):
        self.start = self.camera.get_global_mouse_pos()
        self.dragging = True

    def stop_drag(self):
        self.image = pg.Surface((0, 0))
        self.dragging = False

    def update(self, _delta=0.0):
        if self.dragging:
            mouse = self.camera.get_global_mouse_pos()
            tl = (min(self.start[0], mouse[0]), min(self.start[1], mouse[1]))
            size = (
                abs(self.start[0] - mouse[0]),
                abs(self.start[1] - mouse[1]),
            )
            self.image = Surface(size)
            self.image.set_alpha(128)
            self.rect = self.image.get_rect()
            self.pos = tl
            self.image.fill(self.color)
            pg.draw.rect(
                self.image, "darkgreen", self.rect.move(-self.rect.x, -self.rect.y), 1
            )
        else:
            self.rect = Rect(0, 0, 0, 0)


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
        self.box = SelectBox()

    def process_events(self, event: pg.event.Event) -> bool:
        is_processed = False
        if self.selected:
            is_processed = self.selected.process_events(event)
        if not is_processed:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.box.start_drag()
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.box.stop_drag()
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
