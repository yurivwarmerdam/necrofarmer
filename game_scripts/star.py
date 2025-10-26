from typing import Iterable
from astar import AStar
from scripts.tilemap import Tilemap
from pygame import Vector2
from math import hypot


class WalkPath(AStar):
    def __init__(self, tilemap: Tilemap) -> None:
        super().__init__()
        self.tilemap: Tilemap = tilemap

    def neighbors(self, node: Vector2) -> Iterable:
        # TODO: What about non-orthogonal tiles??
        neighbors = self.tilemap.get_neigbors(node)
        n_iter = neighbors.copy()
        for neighbor in n_iter:
            for layer in self.tilemap.layers:
                properties = self.tilemap.get_tilev_properties(neighbor, layer)
                if not properties.get("can_walk", True):
                    neighbors.remove(neighbor)
        neighbors = [tuple(neighbor) for neighbor in neighbors]
        return neighbors

    def distance_between(self, n1: Vector2, n2: Vector2) -> float:
        # TODO: something about sqrt(2) if neigbors return non-orthogonal cells.
        # Might be equal to heuristic, I think.
        return 1

    def heuristic_cost_estimate(self, current: tuple, goal: tuple) -> float:
        (x1, y1) = current
        (x2, y2) = goal
        return hypot(x2 - x1, y2 - y1)

    def astar_map(self, start, goal):
        pass

    def astar_world(self, start, goal):
        pass


_instance = None


def get_server(map: Tilemap | None = None) -> WalkPath:
    global _instance
    if _instance is None and map is None:
        raise Exception("Star server not yet initiated with a map.")
    elif _instance is None:
        _instance = WalkPath(map)  # type: ignore
    return _instance
