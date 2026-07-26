from game_scripts.group_server import get_group_server
from game_scripts.thopter import Ornithopter
from blinker import signal
from scripts.custom_sprites import NodeSprite


class Spawner:
    def __init__(self) -> None:
        signal("spawn_thopter").connect(self.spawn_thopter, weak=False)
        pass

    def spawn_thopter(self, sender: NodeSprite):
        Ornithopter(sender.pos)
        pass


_instance = None


def get_spawner() -> Spawner:
    global _instance
    if _instance is None:
        _instance = Spawner()  # type: ignore
    return _instance
