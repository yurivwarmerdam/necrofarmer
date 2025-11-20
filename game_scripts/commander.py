import pygame as pg
from pygame import Vector2, Rect, Surface
from pygame.sprite import Sprite
from dataclasses import dataclass
from scripts.camera import Camera, get_camera
from scripts.custom_sprites import NodeSprite
from game_scripts import group_server
from game_scripts.group_server import GroupServer


class SelectBox(NodeSprite):
    def __init__(self) -> None:
        super().__init__(Surface((0, 0)))
        self.color = pg.Color(34, 135, 34)
        self.image.fill(self.color)
        self.image.set_alpha(128)
        self.dragging: bool = False
        self.start = Vector2()
        self.camera: Camera = get_camera()
        self.group_server = group_server.get_server()

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

    def get_overlaps(self):
        collides=pg.sprite.spritecollide(
            self,
            self.group_server.colliders,
            dokill=False,
            collided=pg.sprite.collide_mask,
        )
        print(collides)
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
        self.box = SelectBox()

    def process_events(self, event: pg.event.Event) -> bool:
        is_processed = False
        if self.selected:
            if len(self.selected) == 1:
                is_processed = self.selected[0].process_events(event)
            else:
                # group select. Dunno.
                pass
        if not is_processed and hasattr(event, "button"):
            if event.button == 1:
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.box.start_drag()
                elif event.type == pg.MOUSEBUTTONUP:
                    self.box.get_overlaps()
                    self.box.stop_drag()
            else:
                # check for overlaps
                # unselect/select based on rules
                pass

        return is_processed
