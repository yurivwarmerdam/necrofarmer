from scripts.custom_sprites import AnimatedSprite, integer_scale
from game_scripts.context_panel import ContextPanel
from game_scripts.selectable import Selectable
from scripts import image_server

class Ornithopter(AnimatedSprite, Selectable):
    def __init__(
        self, animations, pos, *groups, anchor="midbottom", offset=..., flip_h=False
    ):
        super().__init__(
            animations, pos, *groups, anchor=anchor, offset=offset, flip_h=flip_h
        )

    @property
    def context_panel(self) -> type[ContextPanel]:
        return OrnithopterPanel


class OrnithopterPanel(ContextPanel):
    def __init__(self, *, commander, context_container):
        super().__init__(
            portrait_id="#ornithopter_button",
            commander=commander,
            context_container=context_container,
        )
