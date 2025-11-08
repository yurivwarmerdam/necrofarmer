from dataclasses import dataclass
from pygame.sprite import Group


@dataclass
class GroupServer:

    RENDER=1
    COLLISION=2
    UPDATE=4

    render_groups: list[Group] = []
    collision_groups: list[Group] = []  # Do I maybe only want one??
    update_groups: list[Group] = []

    def add_render_group():
        pass

    def add_render_groups():
        pass

    def add_group(self,group,*types):
        if self.RENDER in types:
            

        pass

    def add_groups():
        pass


_instance = None


def get_server() -> GroupServer:
    global _instance
    if _instance is None:
        _instance = GroupServer(map)  # type: ignore
    return _instance
