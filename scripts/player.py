from pygame.math import Vector2
from pygame import Surface
from pygame.key import ScancodeWrapper
from scripts.entities import Seed, CustomSprite

FACINGS = [Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0)]


class PlayerEntity(CustomSprite):
    def __init__(self, game, e_type, pos, image, mana=200):
        self.game = game
        self.type = e_type
        self.image=image
        self.rect=image.get_rect()
        self.pos = pos
        self.sprite = image
        self.mana = mana
        self.facing = Vector2(0, -15)

    def update(self, delta: float, input_movement: Vector2, keys: ScancodeWrapper):
        frame_movement = input_movement
        self.pos+=frame_movement
        # self.pos[0] += frame_movement[0]
        # self.pos[1] += frame_movement[1]
        self.mana += 1 * delta
        self.mana = min(self.mana, 200)
        self.facing = (
            input_movement * 15 if input_movement != Vector2(0, 0) else self.facing
        )

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.pos)

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
