from typing import Iterable
from astar import AStar
from scripts.tilemap import Tilemap
from pygame import Vector2


class WalkPath(AStar):
    def __init__(self, tilemap: Tilemap) -> None:
        super().__init__()
        self.tilemap: Tilemap = tilemap

    def neighbors(self, node: Vector2) -> Iterable:
        # TODO: What about non-orthogonal tiles??
        result = []
        neighbors = self.tilemap.get_neigbors(node)
        for neighbor in neighbors:
            for layer in self.tilemap.layers:
                properties = self.tilemap.get_tilev_properties(neighbor, layer)
                if not properties.get("can_walk", True):
                    neighbors.remove(neighbor)
        return result

    def distance_between(self, n1: Vector2, n2: Vector2) -> float:
        # TODO: something about sqrt(2) if neigbors return non-orthogonal cells.
        # Might be equal to heuristic, I think.
        return 1

    def heuristic_cost_estimate(self, current: Vector2, goal: Vector2) -> float:
        return (goal - current).length()
