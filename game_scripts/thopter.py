from scripts.custom_sprites import AnimatedSprite, integer_scale
from game_scripts.ui.context_panel import ContextPanel
from game_scripts.selectable import Selectable
from scripts import image_server
from game_scripts import group_server
from pygame.math import Vector2

from scripts.behaviortree_py.behaviortree import BehaviorTreeFactory
from scripts.entities import ActionStatus
from scripts.behaviortree_py.dummy_nodes import Failer, Succeeder, Talker

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
            groups.behavior_trees,
        )

        # --- BehaviorTree stuff ---
        self.blackboard = {
            "action_status": ActionStatus.IDLE,
            "self": self,
        }  # minimal required set of blackboard entries.
        nodes = {
            "Succeeder": Succeeder,
            "Failer": Failer,
            "Talker": Talker,
        }  # some sample nodes you'll propbably end up using anyway.
        factory = BehaviorTreeFactory()
        factory.register_blackboard(self.blackboard)
        factory.register_nodes(nodes)
        factory.register_conversion_context(
            {"Vector2": Vector2}
        )  # In case nonstandard datatypes are described in tree.xml, provide mappings here.
        self.tree = factory.load_tree_from_xml(
            "trees/ornithopter.xml"
        )  # where your tree is defined

    def tick(self):
        self.tree.tick()

    @property
    def context_panel(self) -> type[ContextPanel]:
        return OrnithopterPanel


class OrnithopterPanel(ContextPanel):
    def __init__(self, *, context_container):
        super().__init__(
            portrait_id="#ornithopter_button",
            context_container=context_container,
        )
