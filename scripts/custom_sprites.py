from typing import Any, Iterable, Optional, override

import pygame as pg
from blinker import signal
from pygame import Vector2, transform
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Group, LayeredUpdates, Sprite
from pygame.surface import Surface
from pygame.transform import scale_by
from pygame.typing import Point


class NodeSprite(Sprite):
    """Generic class for "object-style" sprites.
    Intended to be interacted mostly through pos."""

    def __init__(
        self,
        image: Surface,
        pos: Vector2 = Vector2(0, 0),
        anchor="topleft",
        offset: Vector2 = Vector2(0, 0),
        *groups,
    ):
        super().__init__(*groups)
        self.anchor = anchor
        self.image: Surface = image
        self.rect: Rect = image.get_rect()
        self.offset = offset
        self.pos = pos

    # TODO: this even need to be here...?
    def draw(self, surface):
        print("Am I even being called?")
        surface.blit(self.image, self.rect)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: Vector2 | tuple[int, int]):
        if value is Vector2:
            self._pos = value
        else:
            self._pos = Vector2(value)
        setattr(self.rect, self.anchor, self._pos - self.offset)
        for g in self.groups():
            if isinstance(g, LayeredUpdates):
                g.change_layer(self, self.pos.y)  # add with chosen layer


class AnimationSequence:
    def __init__(self, *frames: Surface, frame_time=200) -> None:
        self.frames = frames
        self.frame_time = frame_time
        self.reset()

    def play(self):
        self.playing = True
        # TODO... now what?

    def reset(self):
        self.current_frame_time = 0
        self.idx = 0

    @property
    def image(self):
        return self.frames[self.idx]

    def tick(self, delta):
        self.current_frame_time += delta
        if self.current_frame_time > self.frame_time:
            self.current_frame_time = self.current_frame_time % self.frame_time
            self.idx = (self.idx + 1) % len(self.frames)
            return self.image


class AnimatedSprite(NodeSprite):
    def __init__(
        self,
        animations: dict[str, AnimationSequence],
        pos: Vector2,
        *groups,
        anchor="midbottom",
        offset=Vector2(0, 0),
        flip_h=False,
    ) -> None:
        self.animations = animations
        self.active_animation = next(iter(animations.values()))
        super().__init__(self.active_animation.image, pos, anchor, offset, *groups)
        self.flip_h = flip_h

    def set_animation(self, name: str):
        self.active_animation = self.animations[name]
        self.image = self.active_animation.image
        pass

    def update(self, delta):
        result = self.active_animation.tick(delta)
        if result:
            self.image = transform.flip(result, True, False) if self.flip_h else result
        # TODO: the following is bad and will break down the line.
        for group in self.groups():
            if isinstance(group, LayeredUpdates):
                group.change_layer(self, self.pos.y)


def tilingscale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Scale a surface to an arbitrary size smoothly.

    tiles the input surface as a way of scaling each dimension as required.
    For shrinkage, the surface is simply clipped to fit the dest_surface.
    The size is a 2 number sequence for (width, height).

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must be the same as the size (width, height) passed
    in, and the same depth and format as the source Surface.
    """
    if dest_surface is not None:
        if dest_surface.size != size:
            raise ValueError("Destination surface doesn't match the provided size")
    else:
        dest_surface = Surface(size, pg.SRCALPHA)
    for x in range(0, dest_surface.width, surface.width):
        for y in range(0, dest_surface.height, surface.height):
            dest_surface.blit(surface, (x, y))
    return dest_surface


def ninepatchscale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
    patch_margain: dict | int = {"left": 0, "right": 0, "top": 0, "bottom": 0},
    scale_func=pg.transform.scale,
) -> Surface:
    """
    Behaves like a scaling func, but should probably be thought of more as a wrapper for some other scaling func.
    """
    if dest_surface is not None:
        if dest_surface.size != size:
            raise ValueError("Destination surface doesn't match the provided size")
    else:
        dest_surface = Surface(size, pg.SRCALPHA).convert_alpha()

    if type(patch_margain) is int:
        patch_margain = {
            "left": patch_margain,
            "right": patch_margain,
            "top": patch_margain,
            "bottom": patch_margain,
        }

    surface_w, surface_h = surface.size
    dest_w, dest_h = size  # non-sequence argument caught by python
    subsurface = surface.subsurface

    surf_center_w = surface_w - (patch_margain["left"] + patch_margain["right"])
    surf_center_h = surface_h - (patch_margain["top"] + patch_margain["bottom"])

    dest_center_w = dest_w - (patch_margain["left"] + patch_margain["right"])
    dest_center_h = dest_h - (patch_margain["top"] + patch_margain["bottom"])

    if (
        min(patch_margain.values()) < 0
        or patch_margain["left"] + patch_margain["right"] > dest_w
        or patch_margain["top"] + patch_margain["bottom"] > dest_h
    ):
        raise ValueError(
            "Corner size must be nonnegative and not greater than the smaller between width and height"
        )
    if not any(patch_margain.values()):  # default to normal scaling if all are 0
        return scale_func(surface, size)

    dest_surface.blit(  # topleft corner
        subsurface(0, 0, patch_margain["left"], patch_margain["top"]), (0, 0)
    )
    dest_surface.blit(  # topright corner
        subsurface(
            surface_w - patch_margain["right"],
            0,
            patch_margain["right"],
            patch_margain["top"],
        ),
        (dest_w - patch_margain["right"], 0),
    )
    dest_surface.blit(  # bottomleft corner
        subsurface(
            0,
            surface_h - patch_margain["bottom"],
            patch_margain["left"],
            patch_margain["bottom"],
        ),
        (0, dest_h - patch_margain["bottom"]),
    )
    dest_surface.blit(  # bottomright corner
        subsurface(
            surface_w - patch_margain["right"],
            surface_h - patch_margain["bottom"],
            patch_margain["right"],
            patch_margain["bottom"],
        ),
        (dest_w - patch_margain["right"], dest_h - patch_margain["bottom"]),
    )

    if patch_margain["top"] > 0:
        dest_surface.blit(  # top side
            scale_func(
                subsurface(
                    patch_margain["left"],
                    0,
                    surf_center_w,
                    patch_margain["top"],
                ),
                (dest_center_w, patch_margain["top"]),
            ),
            (patch_margain["left"], 0),
        )
    if patch_margain["bottom"] > 0:
        dest_surface.blit(  # bottom side
            scale_func(
                subsurface(
                    patch_margain["left"],
                    surface_h - patch_margain["bottom"],
                    surf_center_w,
                    patch_margain["bottom"],
                ),
                (dest_center_w, patch_margain["bottom"]),
            ),
            (patch_margain["left"], dest_h - patch_margain["bottom"]),
        )

    if patch_margain["left"] > 0:
        dest_surface.blit(  # left side
            scale_func(
                subsurface(
                    0,
                    patch_margain["top"],
                    patch_margain["left"],
                    surf_center_h,
                ),
                (patch_margain["left"], dest_center_h),
            ),
            (0, patch_margain["top"]),
        )
    if patch_margain["right"] > 0:
        dest_surface.blit(  # right side
            scale_func(
                subsurface(
                    surface_w - patch_margain["right"],
                    patch_margain["top"],
                    patch_margain["right"],
                    surf_center_h,
                ),
                (patch_margain["right"], dest_center_h),
            ),
            (dest_w - patch_margain["right"], patch_margain["top"]),
        )

    if surf_center_w > 0 and surf_center_h > 0:
        dest_surface.blit(  # central area
            scale_func(
                subsurface(
                    patch_margain["left"],
                    patch_margain["top"],
                    surf_center_w,
                    surf_center_h,
                ),
                (dest_center_w, dest_center_h),
            ),
            (patch_margain["left"], patch_margain["top"]),
        )

    return dest_surface


def integer_scale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
):
    """Scale a surface to the largest integer multiple of surface:size.
    if dimentional ratios of surface and size do not match, takes the smallest of the width and height multiplier.

    Uses the scale_by function, but presents itself as a more regular scale func,
    in order to comply with what something like pygame_gui expects.
    Currently does not support shrinkage.
    The size is a 2 number sequence for (width, height).

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must be the same as the size (width, height) passed
    in, and the same depth and format as the source Surface.
    """

    multiplier = min(size[0] // surface.size[0], size[1] // surface.size[1])

    if dest_surface is not None:
        if dest_surface.size != size:
            raise ValueError("Destination surface doesn't match the provided size")
    else:
        dest_surface = Surface(
            (surface.size[0] * multiplier, surface.size[1] * multiplier)
        )
    scale_by(surface, multiplier, dest_surface)
    return dest_surface


class SignalGroup(Group):
    """
    Regular Group that sends a signal whenever add or remove is called.
    Signal name is provided through kwargs.
    """

    def __init__(
        self, *sprites: Any | AbstractGroup | Iterable, signal_name=""
    ) -> None:
        self.signal = signal(signal_name)
        super().__init__(*sprites)

    @override
    def add(self, *sprites: Any | AbstractGroup | Iterable) -> None:
        super().add(*sprites)
        self.signal.send(self)

    @override
    def remove(self, *sprites: Any | AbstractGroup | Iterable) -> None:
        super().remove(*sprites)
        self.signal.send(self)

    @override
    def empty(self) -> None:
        super().empty()
        self.signal.send(self)
