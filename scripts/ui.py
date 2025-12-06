import pygame_gui
from pygame_gui.core.interfaces import IContainerLikeInterface


class ImageButton(pygame_gui.elements.UIButton):
    def __init__(
        self,
        pos,
        outline_sprites,
        fill_sprite,
        container: IContainerLikeInterface | None = None,
    ):
        super().__init__(
            relative_rect=outline_sprites[(0, 0)].get_rect(),
            text="",
            object_id="hello_button",
            container=container,
        )
        self.normal_images = [outline_sprites[(0, 0)], fill_sprite]
        self.hovered_images = [outline_sprites[(0, 0)], fill_sprite]
        self.disabled_images = [outline_sprites[(2, 0)], fill_sprite]
        self.selected_images = [outline_sprites[(1, 0)], fill_sprite]
        self.set_relative_position(pos)
        self.rebuild()