from pygame.math import Vector2
from pygame import Surface
from pygame.key import ScancodeWrapper
from scripts.entities import Seed


class PlayerEntity:
    def __init__(self, game, e_type, pos, size, sprite, mana=200):
        self.game = game
        self.type = e_type
        self.pos = pos
        self.sprite = sprite
        self.size = size
        self.velocity = Vector2(0, 0)
        self.mana = mana

    def update(self, delta: float, input_movement: Vector2, keys: ScancodeWrapper):
        frame_movement = input_movement + self.velocity
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        self.mana += 1 * delta
        self.mana = min(self.mana, 200)

    def render(self, surface: Surface):
        surface.blit(self.sprite, self.pos)

    def action(self):
        if self.mana >= 50:
            self.spawn_seed()
            self.mana -= 50

    def spawn_seed(self):
        self.game.seeds.add(
            Seed(self, self.game.assets["seed"], self.game.player.pos),
        )


class JobCoordinator():
    
    pass