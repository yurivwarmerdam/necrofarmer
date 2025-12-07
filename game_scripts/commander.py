import pygame as pg
from pygame import Vector2, Rect, Surface
from pygame.sprite import Sprite, Group
from scripts.camera import Camera, get_camera
from scripts.custom_sprites import NodeSprite
from game_scripts import group_server
from game_scripts.group_server import GroupServer
from scripts.custom_sprites import SignalGroup
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
        self.selected = SignalGroup(signal_name="selected_changed")
        self.dragging = False
        self.select_box = SelectBox()
        self.box = SelectBox()
        self.group_server = group_server.get_server()
        self.camera = get_camera()

    def process_events(self, event: pg.event.Event) -> bool:
        # -- motion --
        # buttons is kind of a button mask when event is mousemotion
        if event.type == pg.MOUSEMOTION and event.buttons[0] == 1:
            self.box.handle_drag(event)
            return True
        # -- mouse buttons --
        if event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
            if self.selected:
                processed = any(
                    [sprite.process_events(event) for sprite in self.selected]
                )
                if processed:
                    return True
            if event.button == 1:
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.box.start_drag()
                    return True
                elif self.box.dragging:
                    self.do_box_select()
                    return True
                else:
                    collided_sprites = pointcollide(
                        self.camera.get_global_mouse_pos(), self.group_server.colliders
                    )
                    self.selected.empty()
                    if collided_sprites:
                        self.selected.add(collided_sprites[0])
                    return True
        return False

    def do_box_select(self):
        self.selected.empty()
        for collide in self.box.get_collides():
            if isinstance(collide, Sprite):
                collide.add(self.selected)
        self.box.stop_drag()
        pass


def pointcollide(point, group, collide_callback=None):
    """Kind of extra for now. However, it mostly follows the pattern of *collide functions in official pygame."""
    default_callback = pointcollide_mask

    if collide_callback is not None:
        return [sprite for sprite in group if collide_callback(point, sprite)]

    return [sprite for sprite in group if default_callback(point, sprite)]

    pass


def pointcollide_mask(point: tuple[int, int], sprite: Sprite) -> bool:
    """
    collision detection between a point and a sprite, using masks.

    pygame.sprite.collide_mask(point, sprite): bool

    Tests for collision between a point and a sprite by testing if the sprites' bitmask
    is occupied at the point. If the sprite has a "mask" attribute, that is used as the mask;
    otherwise, a mask is created from the sprite image. Intended to be passed
    as a collided callback function to pointcollide. Sprites must
    have a "rect" and an optional "mask" attribute.
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
