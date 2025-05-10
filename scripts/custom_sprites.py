from pygame.sprite import Sprite
from pygame import Vector2
from pygame.surface import Surface
from pygame.rect import Rect


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
        self.offset = offset
        self.pos = pos

        self.facing = Vector2(0, -15)
        super().__init__(*groups)

    def draw(self,surface):
        surface.blit(self.image, self.rect)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: Vector2):
        self._pos = value
        setattr(self.rect, self.anchor, self.pos - self.offset)
        


# class TileSprite(Sprite):
#     """Generic class for tile sprites.
#     Intended to be relatively static during their lifetime."""

#     def __init__(self, pos, image, *groups):
#         super().__init__(*groups)
#         self.image = image
#         self.rect = self.image.get_rect(topleft=pos)
