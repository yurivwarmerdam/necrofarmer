from dataclasses import dataclass, field
from pygame.sprite import AbstractGroup, Group, Sprite


@dataclass
class GroupServer:
    RENDER = 1
    COLLISION = 2
    UPDATE = 4

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
    # Could be edited to be collision groups by making a dict,
    # and adding collision layers if needed.
    colliders: Group = Group()
    update: Group = Group()

    def add_render(self, groups: dict[str, Group] | dict[str, AbstractGroup]):
        print(type(self.render_groups))
        self.render_groups = self.render_groups | groups.copy()

    def add_collider_sprite(self, entity: Sprite):
        self.colliders.add(entity)

    def add_update_sprite(self, entity: Sprite):
        self.update.add(entity)


_instance = None


def get_server() -> GroupServer:
    global _instance
    if _instance is None:
        _instance = GroupServer()  # type: ignore
    return _instance
