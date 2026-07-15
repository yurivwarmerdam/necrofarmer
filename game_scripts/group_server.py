from dataclasses import dataclass, field

from pygame.sprite import AbstractGroup, Group, Sprite
from scripts.behaviortree_py.util_pygame import BTGroup
from pygame.sprite import spritecollide
from scripts.utils import pointcollide


@dataclass
class GroupServer:
    # --------------
    # Render groups
    # --------------
    #
    # dict of groups, since rendering happens in layers.
    render_groups: dict[str, Group] = field(default_factory=dict)

    collide_groups: dict[int, Group] = field(
        default_factory=lambda: {
            1: Group(),
            2: Group(),
            4: Group(),
            8: Group(),
            16: Group(),
            32: Group(),
        }
    )
    # --------------
    # function-specific groups
    # --------------
    #
    colliders: Group = Group()
    update: Group = Group()
    behavior_trees: BTGroup = BTGroup()

    def add_render_groups(self, groups: dict[str, Group] | dict[str, AbstractGroup]):
        self.render_groups = self.render_groups | groups.copy()

    def add_collider_sprite(self, sprite: Sprite):
        mask = sprite.collision_mask if hasattr(sprite, "collision_mask") else 0
        for group in self.get_collide_groups_by_mask(mask):
            group.add(sprite)
        self.colliders.add(sprite)

    def add_group_to_colliders(self, group: Group):
        """Add any sprites in the provided group to relevant collision layers.
        Only adds sprites that have a collision_mask property"""
        for sprite in group.sprites():
            if hasattr(sprite, "collision_mask"):
                self.add_collider_sprite(sprite)

    def add_update_sprite(self, entity: Sprite):
        """for sprites that should be processed with an update method"""
        self.update.add(entity)

    def add_behavior_tree_sprite(self, entity: Sprite):
        self.behavior_trees.add(entity)

    def get_collide_groups_by_mask(self, collision_mask: int) -> list[Group]:
        """Returns a list of all groups that match the sprite's collision mask."""
        return [
            group
            for flag, group in self.collide_groups.items()
            if (collision_mask & flag)
        ]

    def sprite_collide(self, sprite: Sprite) -> list[Sprite]:
        """collisions between a sprite and all groups matching their collision_mask."""
        collisions = set()
        mask = sprite.collide_mask if hasattr(sprite, "collide_mask") else 0
        for group in self.get_collide_groups_by_mask(mask):
            hits = spritecollide(sprite, group, False)
            if hits:
                collisions.update(hits)
        return list(collisions)

    def point_collide(self, point: tuple[int, int], collision_mask=64) -> list[Sprite]:
        """collisions between a point and all groups matching the provided collision_mask."""
        collisions = set()

        for group in self.get_collide_groups_by_mask(collision_mask):
            hits = pointcollide(point, group)
            if hits:
                collisions.update(hits)
        return list(collisions)


_instance = None


def get_group_server() -> GroupServer:
    global _instance
    if _instance is None:
        _instance = GroupServer()  # type: ignore
    return _instance
