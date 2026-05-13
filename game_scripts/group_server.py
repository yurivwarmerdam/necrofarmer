from dataclasses import dataclass, field

from pygame.sprite import AbstractGroup, Group, Sprite
from scripts.behaviortree_py.util_pygame import BTGroup


@dataclass
class GroupServer:
    # --------------
    # Render groups
    # --------------
    #
    # only dict group, since rendering happens in layers.
    render_groups: dict[str, Group] = field(default_factory=dict)

    # --------------
    # function-specific groups
    # --------------
    #
    # thought: Could be edited to be collision groups by making a dict,
    # and adding collision layers if needed.
    colliders: Group = Group()
    update: Group = Group()
    behavior_trees: BTGroup = BTGroup()

    def add_render(self, groups: dict[str, Group] | dict[str, AbstractGroup]):
        self.render_groups = self.render_groups | groups.copy()

    def add_collider_sprite(self, entity: Sprite):
        self.colliders.add(entity)

    def add_update_sprite(self, entity: Sprite):
        self.update.add(entity)

    def add_behavior_tree_sprite(self, entity: Sprite):
        self.behavior_trees.add(entity)


_instance = None


def get_group_server() -> GroupServer:
    global _instance
    if _instance is None:
        _instance = GroupServer()  # type: ignore
    return _instance
