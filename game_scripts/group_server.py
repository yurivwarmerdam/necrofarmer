from dataclasses import dataclass
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
    render_groups: dict[str, Group]

    # --------------
    # function-specific groups
    # --------------
    #
    # Could be edited to be collision groups by making a dict,
    # and adding collision layers if needed.
    collision: Group = Group()
    update: Group = Group()

    def add_render(self, groups: dict[str, Group]|dict[str, AbstractGroup]):
        self.render_groups = self.render_groups | groups.copy()

    def add_collision(self, entity: Sprite):
        self.collision.add(entity)

    def add_update(self, entity: Sprite):
        self.update.add(entity)


_instance = None


def get_server() -> GroupServer:
    global _instance
    if _instance is None:
        _instance = GroupServer(map)  # type: ignore
    return _instance
