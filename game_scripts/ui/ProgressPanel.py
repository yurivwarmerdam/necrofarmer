from game_scripts.commander import get_commander
from game_scripts.ui.ui_elements import BackgroundPanel
from scripts.custom_sprites import integer_scale
from scripts.ui_shim import UIButton


import pygame as pg
from pygame_gui.elements import UIProgressBar


class ProgressPanel(BackgroundPanel):
    def __init__(self, context_container, cancel_command, visible: int = 1):
        super().__init__(pg.Rect(120, -3, 160, 99), context_container, visible=visible)

        self.cancel_button = UIButton(
            pg.Rect(0, 41, 54, 46),
            text="",
            object_id="#cancel_button",
            scale_func=integer_scale,
            container=self.get_container(),
            command=cancel_command,
            # visible=True,
        )
        self.progress_bar = UIProgressBar(
            pg.Rect(0, 0, 150, 40), container=self.get_container()
        )
        self.set_progress(0)

    def set_progress(self, progress):
        self.progress_bar.set_current_progress(progress)
