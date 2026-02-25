from dataclasses import dataclass

from pygame import Vector2

from scripts.custom_sprites import AnimationSequence
from scripts.utils import load_image, sheet_to_sprites


@dataclass
class ImageServer:
    def __init__(self) -> None:
        # TODO: Consider loading images trough some sort of yaml.
        # Alternative idea is to load this through tiled and pytmx.
        self.sprites = sheet_to_sprites(
            load_image("art/tardigrade.png"), Vector2(80, 80)
        )
        self.animations = {}

        self.animations["tardigrade_0"] = AnimationSequence(
            self.sprites[(0, 0)],
            self.sprites[(1, 0)],
            self.sprites[(2, 0)],
            self.sprites[(3, 0)],
        )
        self.animations["tardigrade_1"] = AnimationSequence(
            self.sprites[(0, 1)],
            self.sprites[(1, 1)],
            self.sprites[(2, 1)],
            self.sprites[(3, 1)],
        )
        self.animations["tardigrade_2"] = AnimationSequence(
            self.sprites[(0, 2)],
            self.sprites[(1, 2)],
            self.sprites[(2, 2)],
            self.sprites[(3, 2)],
        )
        self.animations["tardigrade_3"] = AnimationSequence(
            self.sprites[(0, 3)],
            self.sprites[(1, 3)],
            self.sprites[(2, 3)],
            self.sprites[(3, 3)],
        )


_instance = None


def get_server() -> ImageServer:
    global _instance
    if _instance is None:
        _instance = ImageServer()
    return _instance
