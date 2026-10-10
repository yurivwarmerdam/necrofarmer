from blinker import signal

from game_scripts.thopter import Thopter
from scripts.custom_sprites import NodeSprite
from scripts.group_server import get_group_server
from game_scripts.game_tilemap import get_tilemap


class Spawner:
    def __init__(self) -> None:
        print("spawner")
        signal("spawn_thopter").connect(self.spawn_thopter, weak=False)
        signal("start_build_thopter").connect(self.start_build_thopter, weak=False)
        signal("spawn_sawmill").connect(self.spawn_sawmill, weak=False)
        self.group_server = get_group_server()
        self.tilemap = get_tilemap()
        pass

    def start_build_thopter(self, sender: NodeSprite):
        Thopter(sender.pos, preload=True)

    def spawn_thopter(self, sender: NodeSprite):
        # TODO: thechnically more efficient to reassign existing thopter to regular groups
        # instead of removing and adding one.
        unfinished_l = self.group_server.typed_groups["_Thopter"].sprites()
        val = unfinished_l[0] if len(unfinished_l) > 0 else None
        print(unfinished_l, val)
        if not val:
            raise Exception("finishing construction without ever starting")
        val.kill()
        Thopter(sender.pos)
        pass

    def spawn_sawmill(self, sender):
        print("Oh yeah!")
        pass


_instance = None


def get_spawner() -> Spawner:
    global _instance
    if _instance is None:
        _instance = Spawner()  # type: ignore
    return _instance
