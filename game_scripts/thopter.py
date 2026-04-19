from scripts.custom_sprites import AnimatedSprite, integer_scale
from game_scripts.context_panel import ContextPanel
from game_scripts.selectable import Selectable
from scripts import image_server
from game_scripts import group_server

# TODO:
# - add btree
# - def move (maybe with random target position button)
# - def load
# - def unload
# - def idle (land)
# - def take off


class Ornithopter(AnimatedSprite, Selectable):
    def __init__(self, pos):
        img_server = image_server.get_image_server()
        groups = group_server.get_group_server()
        super().__init__(
            {
                "0": img_server.animations["thopter_0"],
                "1": img_server.animations["thopter_1"],
                "2": img_server.animations["thopter_2"],
                "3": img_server.animations["thopter_3"],
            },
            pos,
            groups.update,
            groups.colliders,
            groups.render_groups["active"],
        )

    @property
    def context_panel(self) -> type[ContextPanel]:
        return OrnithopterPanel


class OrnithopterPanel(ContextPanel):
    def __init__(self, *, context_container):
        super().__init__(
            portrait_id="#ornithopter_button",
            context_container=context_container,
        )
