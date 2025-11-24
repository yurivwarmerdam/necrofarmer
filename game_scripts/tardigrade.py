import pygame as pg
from scripts.custom_sprites import AnimatedSprite
from scripts import image_server
from pygame import Vector2
from collections import deque


# Needs access to:
# - groups
# v tilemap
# v star (already has a server)
class Tardigrade(AnimatedSprite):
    def __init__(self, pos: Vector2, *groups):
        self.img_server = image_server.get_server()

        super().__init__(
            {
                "0": self.img_server.animations["tardigrade_0"],
                "1": self.img_server.animations["tardigrade_1"],
                "2": self.img_server.animations["tardigrade_2"],
                "3": self.img_server.animations["tardigrade_3"],
            },
            pos,
            *groups,
            anchor="center",
            offset=Vector2(0, 10),
        )

        self.move_goal = None
        self.path = []

    def process_events(self, event: pg.event.Event) -> bool:
        if hasattr(event, "button") and event.button == 3:
            print("processing I need to start walking")
            return True
        else:
            return False

    def set_path(self, goal: Vector2):
        start = tuple(tilemap.world_to_map(sprite.pos))
        move_goal = camera.get_global_mouse_pos()
        goal = tuple(tilemap.world_to_map(move_goal))
        path = path_planner.astar(start, goal) or []
        path = deque([tilemap.map_to_world(*pos) for pos in path])

    def move_towards(self, source: Vector2, target: Vector2, by: float) -> Vector2:
        delta = target - source
        dist = delta.length()
        if dist <= by or dist == 0:
            return target
        return source + delta.normalize() * by

    def move_along_path(
        self, source: Vector2, path: deque[Vector2], by: float
    ) -> Vector2:
        """Note: this consumes path when waypoints are reached."""
        EPS = 1e-9
        result = source.copy()
        while by > EPS and path:
            intermediate = self.move_towards(result, path[0], by)
            by -= (intermediate - result).length()
            result = intermediate
            if path[0] == result:
                path.popleft()
        return result
