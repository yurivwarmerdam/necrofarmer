from dataclasses import dataclass
from pygame.sprite import Group


@dataclass
class GroupServer:
    render_groups: list[Group]
