import pygame as pg
from pygame import Vector2, Rect, Surface
from pygame.sprite import Sprite, Group
from dataclasses import dataclass
from scripts.camera import Camera, get_camera
from scripts.custom_sprites import NodeSprite
from game_scripts import group_server
from game_scripts.group_server import GroupServer

from pygame.mask import from_surface


class SelectBox(NodeSprite):
    def __init__(self) -> None:
        super().__init__(Surface((0, 0)))
        self.color = pg.Color(34, 135, 34)
        self.image.fill(self.color)
        self.image.set_alpha(128)
        self.dragging: bool = False
        self.start: Vector2 | None = None
        self.camera: Camera = get_camera()
        self.group_server = group_server.get_server()

    def start_drag(self):
        self.start = self.camera.get_global_mouse_pos()

    def stop_drag(self):
        self.image = pg.Surface((0, 0))
        self.start = None
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
    Defers inputs to
    """

    def __init__(self):
        self.selected = Group()
        self.dragging = False
        self.select_box = SelectBox()
        self.box = SelectBox()
        self.group_server = group_server.get_server()
        self.camera = get_camera()

    def process_events(self, event: pg.event.Event) -> bool:
        is_processed = False
        # button is kind of a button mask when event is mousemotion
        if event.type == pg.MOUSEMOTION and event.buttons[0] == 1:
            self.box.handle_drag(event)
            is_processed = True
        if event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
            if self.selected:
                for sprite in self.selected:
                    is_processed = sprite.process_events(event)
            if not is_processed:
                if event.button == 1:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.box.start_drag()
                        is_processed = True
                    elif self.box.dragging:
                        self.do_box_select()
                        is_processed = True
                    else:
                        self.handle_click()
            else:
                # check for overlaps
                # unselect/select based on rules
                pass

        return is_processed

    def do_box_select(self):
        for collide in self.box.get_collides():
            if isinstance(collide, Sprite):
                collide.add(self.selected)
        self.box.stop_drag()
        pass

    def handle_click(self):
        """Handle it my own damn self."""
        print("My own damn self!")
        for sprite in self.group_server.colliders:
            collide = pointcollide_mask(self.camera.get_global_mouse_pos(), sprite)
            print(collide)


def pointcollide_mask(point: tuple[int, int], sprite: Sprite) -> bool:
    """
    REWRITE THIS!
    collision detection between two sprites, using masks.

    pygame.sprite.collide_mask(SpriteLeft, SpriteRight): bool

    Tests for collision between two sprites by testing if their bitmasks
    overlap. If the sprites have a "mask" attribute, that is used as the mask;
    otherwise, a mask is created from the sprite image. Intended to be passed
    as a collided callback function to the *collide functions. Sprites must
    have a "rect" and an optional "mask" attribute.

    New in pygame 1.8.0

    """
    xoffset = point[0] - sprite.rect[0]
    yoffset = point[1] - sprite.rect[1]
    try:
        mask = sprite.mask
    except AttributeError:
        mask = from_surface(sprite.image)

    if (
        xoffset < 0
        or xoffset >= mask.get_size()[0]
        or yoffset < 0
        or yoffset >= mask.get_size()[1]
    ):
        return False
    return bool(mask.get_at((xoffset, yoffset)))
