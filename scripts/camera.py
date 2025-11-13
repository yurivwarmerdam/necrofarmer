import pygame as pg
from pygame import Surface
from pygame.color import Color
from pygame.math import Vector2
from pygame.sprite import Group, LayeredUpdates


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
        # not using this yet. Goal is to use it for scale operations, prolly
        self.buffer = Surface(self.display.get_size())

    def get_global_mouse_pos(self):
        return Vector2(pg.mouse.get_pos()) + self.pos

    def draw_all(self):
        self.display.fill(self.bg_color)
        for group in self.render_layers:
            self.draw_layer(self.render_layers[group])
        self.ui.draw(self.display)

    def draw_layer(self, layer: Group):
        """Adapted from pygame's cannonical draw logic:
        draw all sprites onto the surface

        Group.draw(surface, special_flags=0): return Rect_list

        Draws all of the member sprites onto the given surface.

        """
        if layer is LayeredUpdates:
            sprites = sorted(layer.sprites(), key=lambda sprite: sprite.pos.y)
        else:
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

    def draw_to_screen(self):
        
        pass

_instance = None


def initialize_camera(
    render_layers: dict[str, Group],
    ui: Group,
    display: Surface,
    pos=Vector2(0, 0),
    bg_color: Color = Color("blue1"),
) -> Camera:
    global _instance
    _instance = Camera(render_layers, ui, display, pos, bg_color)
    return _instance


def get_camera() -> Camera:
    global _instance
    if _instance is None:
        raise Exception("Camera server not yet initiated.")
    return _instance

# do I want/need this? Maybe for mouse pos math?
# _instance = None


# def instantiate(
#     render_layers: dict[str, Group],
#     ui: Group,
#     display: Surface,
#     pos=Vector2(0, 0),
#     bg_color: Color = Color("blue1"),
# ):
#     _instance = Camera(
#         render_layers,
#         ui,
#         display,
#         pos,
#         bg_color,
#     )


# def get_server() -> Camera:
#     global _instance
#     if _instance is None:
#         raise Exception("Camera server not yet initiated.")
#     return _instance
