from scripts.custom_sprites import AnimatedSprite
from scripts import image_server
from pygame import Vector2
from pygame.sprite import Group


class Tardigrade(AnimatedSprite):
    def __init__(self, pos: Vector2, *groups):
        self.img_server = image_server.get_server()

        super().__init__(
            {
                "0": self.img_server.animations["tardigrade_0"],
                "1": self.img_server.animations["tardigrade_1"],
                "2": self.img_server.animations["tardigrade_2"],
                "3": self.img_server.animations["tardigrade_3"],
            },
            pos,
            *groups,
            anchor="center",
            offset=Vector2(0, 10),
        )

        self.move_goal = None
        self.path = []

    def set_path(self,goal:Vector2):

        pass
