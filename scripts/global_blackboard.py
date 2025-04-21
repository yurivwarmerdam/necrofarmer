import asyncio
from scripts.player import PlayerEntity

class global_blackboard:
    """
    This thing's a singleton. Allows me to have a single bb to talk talk.
    """

    _instance = None
    player:PlayerEntity = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.loop = asyncio.get_event_loop()
