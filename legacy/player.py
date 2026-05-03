from pygame.key import ScancodeWrapper
from pygame.math import Vector2

from scripts.custom_sprites import NodeSprite
from scripts.entities import Seed

FACINGS = [Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0)]


class PlayerEntity(NodeSprite):
    def __init__(
        self,
        image,
        pos,
        *groups,
        anchor="midbottom",
        offset=Vector2(0, -5),
        mana=200,
    ):
        super().__init__(image, pos, anchor, offset, *groups)
        self.mana = mana
        self.facing = Vector2(0, -1)

    def update(self, delta: float, input_movement: Vector2, keys: ScancodeWrapper):
        frame_movement = input_movement
        self.pos += frame_movement
        # self.pos[0] += frame_movement[0]
        # self.pos[1] += frame_movement[1]
        self.mana += 1 * delta
        self.mana = min(self.mana, 200)
        self.facing = (
            input_movement * 15 if input_movement != Vector2(0, 0) else self.facing
        )

    def action1(self):
        if self.mana >= 50:
            self.spawn_seed()
            self.mana -= 50

    def action2(self):
        print(f"face: {self.facing}")
        return

    def spawn_seed(self):
        self.game.seeds.add(
            Seed(self, self.game.assets["seed"], self.game.player.pos),
        )
