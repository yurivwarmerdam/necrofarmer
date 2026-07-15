import pygame as pg
from blinker import signal
from pygame import Rect, Surface, Vector2
from pygame.sprite import Group, Sprite
from pygame_gui.core import UIElement

from game_scripts.group_server import get_group_server
from scripts.camera import Camera, get_camera
from scripts.custom_sprites import NodeSprite
# from scripts.utils import pointcollide
from game_scripts.selectable import Selectable


class SelectBox(NodeSprite):
    def __init__(self) -> None:
        super().__init__(Surface((0, 0)))
        self.color = pg.Color(34, 135, 34)
        self.image.fill(self.color)
        self.image.set_alpha(128)
        self.dragging: bool = False
        self.start: Vector2 | None = None
        self.camera: Camera = get_camera()
        self.group_server = get_group_server()

    def start_click(self):
        self.start = self.camera.get_global_mouse_pos()

    def stop_drag(self):
        self.image = pg.Surface((0, 0))
        self.start = None
        self.dragging = False

    def has_started_click(self):
        return self.start is not None

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

    def handle_drag(self, event: pg.event.Event):
        """
        Please only feed me mouse motion. I am a picky eater.
        """
        if self.start:
            travel = self.start - self.camera.get_global_mouse_pos()
            if travel.length() > 10:
                self.dragging = True
            else:
                self.dragging = False

    def get_collides(self):
        collides = pg.sprite.spritecollide(
            self,
            self.group_server.colliders,
            dokill=False,
            collided=pg.sprite.collide_mask,
        )
        return collides


class Commander:
    """
    Keeps track of any selected units.
    Defers inputs to special (used for debug menu, maybe popup minigames?)
    Defers inputs to selected
    """

    def __init__(self):
        self.debug: Sprite | UIElement | None = None
        self.selected = Group()
        self.dragging = False
        self.select_box = SelectBox()
        self.box = SelectBox()
        self.group_server = get_group_server()
        self.camera = get_camera()
        self.selected_changed = signal("selected_changed")

    def process_events(self, event: pg.event.Event) -> bool:
        # -- motion --
        # buttons is kind of a button mask when event is mousemotion
        if event.type == pg.MOUSEMOTION and event.buttons[0] == 1:
            self.box.handle_drag(event)
            return True
        # -- mouse buttons --
        if event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
            processed = []
            if self.debug:
                if hasattr(self.debug, "process_events"):
                    processed.append(self.debug.process_events(event))
            elif self.selected and not any(processed):
                for sprite in self.selected:
                    if hasattr(sprite, "process_events"):
                        processed.append(sprite.process_events(event))
            processed = any(processed)
            if processed:
                return True
            if event.button == 1:
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.box.start_click()
                    return True
                elif self.box.dragging:
                    self.do_box_select()
                    return True
                else:
                    if self.box.has_started_click():
                        collided_sprites = self.get_mouse_collisions()
                        self.unselect_all()
                        if collided_sprites:
                            self.select(collided_sprites[0])
                        self.box.stop_drag()
                        return True
        return False

    def unselect_all(self):
        if self.selected:
            self.selected.empty()
            self.selected_changed.send(self)

    def select(self, sprites: Sprite | list):
        self.selected.add(sprites)
        self.selected_changed.send(self)

    def unselect(self, sprites: Sprite | list):
        self.selected.remove(sprites)
        self.selected_changed.send(self)

    def do_box_select(self):
        self.selected.empty()
        # TODO: Is this test even needed?
        for collide in self.box.get_collides():
            if isinstance(collide, Selectable):
                collide.add(self.selected)
        self.box.stop_drag()
        self.selected_changed.send(self)

    def get_mouse_collisions(self):
        pos = self.camera.get_global_mouse_pos()
        return self.group_server.point_collide(
            (pos.x, pos.y),
            1,
        )


_instance = None


def get_commander() -> Commander:
    global _instance
    if _instance is None:
        _instance = Commander()
    return _instance
