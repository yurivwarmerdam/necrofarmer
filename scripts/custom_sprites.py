from pygame.sprite import Sprite
from pygame import Vector2
from pygame.surface import Surface
from pygame.rect import Rect
from pygame import transform


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
        self.anchor = anchor
        self.image: Surface = image
        self.rect: Rect = image.get_rect()
        print(self.rect)
        self.offset = offset
        self.pos = pos

        super().__init__(*groups)

    def draw(self,surface):
        surface.blit(self.image, self.rect)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: Vector2):
        self._pos = value
        setattr(self.rect, self.anchor, self._pos - self.offset)
        


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
            # print(self.idx)
            return self.image


class AnimatedSprite(NodeSprite):
    def __init__(
        self,
        animations: dict[str, AnimationSequence],
        pos: Vector2,
        *groups,
        flip_h=False,
    ) -> None:
        super().__init__(*groups)
        self.animations = animations
        self.active_animation = next(iter(animations.values()))
        self.image = self.active_animation.image
        self.rect = self.image.get_rect()
        self.anchor="topleft"
        self.offset=Vector2(0,0)
        self.pos = pos
        self.flip_h = flip_h

    def set_animation(self, name: str):
        self.active_animation = self.animations[name]
        self.image = self.active_animation.image
        pass

    def update(self, delta) -> None:
        result = self.active_animation.tick(delta)
        if result:
            self.image = transform.flip(result, True, False) if self.flip_h else result

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: Vector2):
        self._pos = value
        setattr(self.rect, self.anchor, self.pos - self.offset)
        