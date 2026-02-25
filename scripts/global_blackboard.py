import asyncio

from pygame.sprite import Group

from game_scripts.world_tilemap import WorldTilemap
from scripts.player import PlayerEntity


class global_blackboard:
    """
    This thing's a singleton. Allows me to have a single bb to talk talk.
    """

    _instance = None

    player: PlayerEntity = None
    tilemap: WorldTilemap = None
    seeds: Group = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.loop = asyncio.get_event_loop()
