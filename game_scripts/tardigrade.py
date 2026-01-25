import pygame as pg
from scripts.custom_sprites import AnimatedSprite
from game_scripts import group_server
from scripts.camera import get_camera
from game_scripts import entity_tilemap
from game_scripts import star
from scripts import image_server
from pygame import Vector2
from collections import deque
from random import randint
from game_scripts.context_panel import ContextPanel
from game_scripts.selectable import Selectable

# Needs access to:
# - groups
# v tilemap
# v star (already has a server)
class Tardigrade(AnimatedSprite,Selectable):
    def __init__(self, pos: Vector2):
        img_server = image_server.get_server()
        groups = group_server.get_server()
        super().__init__(
            {
                "0": img_server.animations["tardigrade_0"],
                "1": img_server.animations["tardigrade_1"],
                "2": img_server.animations["tardigrade_2"],
                "3": img_server.animations["tardigrade_3"],
            },
            pos,
            groups.update,
            groups.colliders,
            groups.render_groups["active"],
            anchor="center",
            offset=Vector2(0, 10),
        )

        self.camera = get_camera()
        self.tilemap = entity_tilemap.get_server()
        self.path_planner = star.get_server()

        # self.move_goal = None
        self.path = []

    def update(self, delta):
        # gotta call super because it handles animation frame. May want to separate that out...?
        super().update(delta)

        if randint(0, 100) > 99:
            self.set_animation(str(randint(0, 3)))
            self.flip_h = bool(randint(0, 1))

        if self.path:
            self.pos = self.move_along_path(self.pos, self.path, delta)

    def process_events(self, event: pg.event.Event) -> bool:
        if (
            hasattr(event, "button")
            and event.type == pg.MOUSEBUTTONUP
            and event.button == 3
        ):
            self.path = self.plan_path()
            return True
        else:
            return False

    def plan_path(self):
        start = tuple(self.tilemap.world_to_map(self.pos))
        move_goal = self.camera.get_global_mouse_pos()
        goal = tuple(self.tilemap.world_to_map(move_goal))
        path = self.path_planner.astar(start, goal) or []
        path = deque([self.tilemap.map_to_world(*waypoint) for waypoint in path])
        return path

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
        move_speed = 0.1
        by *= move_speed
        result = source.copy()
        while by > EPS and path:
            intermediate = self.move_towards(result, path[0], by)
            by -= (intermediate - result).length()
            result = intermediate
            if path[0] == result:
                path.popleft()
        return result

class TardigradePanel(ContextPanel):
    pass