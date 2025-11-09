from dataclasses import dataclass
from pygame.sprite import Group, Sprite


@dataclass
class GroupServer:
    RENDER = 1
    COLLISION = 2
    UPDATE = 4

    render_groups: dict[str, Group]

    # --------------
    # function-specific groups
    # --------------
    #
    # Could be edited to be collision groups by making a dict,
    # and adding collision layers if needed
    collision: Group = Group()
    update: Group = Group()

    def init_render_groups(self, groups: dict[str, Group]):
        self.render_groups = groups
        pass

    def add_to_render_group(self, entity: Sprite, layer_name: str):
        self.render_groups[layer_name].add(Sprite)

    def add_to_collision(self, entity: Sprite):
        self.collision.add(entity)

    def add_to_update(self, entity: Sprite):
        self.update.add(entity)


_instance = None


def get_server() -> GroupServer:
    global _instance
    if _instance is None:
        _instance = GroupServer(map)  # type: ignore
    return _instance
