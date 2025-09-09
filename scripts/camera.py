import pygame as pg
from pygame import Surface
from pygame.color import Color
from pygame.math import Vector2
from pygame.sprite import Group


class Camera:
    # relevant source:
    # https://github.com/clear-code-projects/Pygame-Cameras/blob/main/camera.py
    def __init__(
        self,
        render_layers: dict[str, Group],
        ui: Group,
        display: Surface,
        pos=Vector2(0, 0),
        bg_color: Color = Color("blue1"),
    ) -> None:
        self.pos = pos
        self.render_layers = render_layers
        self.ui = ui
        self.display = display
        self.bg_color = bg_color

    def get_global_mouse_pos(self):
        return Vector2(pg.mouse.get_pos()) + self.pos

    def draw_all(self):
        self.display.fill(self.bg_color)
        for group in self.render_layers:
            if group == "active":
                sorted(self.render_layers[group].sprites(), key= lambda sprite: sprite.pos)
            self.draw_layer(self.render_layers[group])
        self.ui.draw(self.display)

    def draw_layer(self, layer: Group):
        """Adapted from pygame's cannonical draw logic:
        draw all sprites onto the surface

        Group.draw(surface, special_flags=0): return Rect_list

        Draws all of the member sprites onto the given surface.

        """
        sprites = layer.sprites()

        if hasattr(self.display, "blits"):
            layer.spritedict.update(
                zip(
                    sprites,
                    self.display.blits(
                        (spr.image, spr.rect.move(-self.pos.x, -self.pos.y), None, 0)
                        for spr in sprites  # type: ignore
                    ),
                )
            )
        else:
            for spr in sprites:
                layer.spritedict[spr] = self.display.blit(
                    spr.image, spr.rect.move(-self.pos.x, -self.pos.y), None, 0
                )
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
