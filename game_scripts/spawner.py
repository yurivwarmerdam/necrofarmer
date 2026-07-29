from game_scripts.group_server import get_group_server
from game_scripts.thopter import Ornithopter
from blinker import signal
from scripts.custom_sprites import NodeSprite


class Spawner:
    def __init__(self) -> None:
        signal("spawn_thopter").connect(self.spawn_thopter, weak=False)
        signal("start_build_thopter").connect(self.start_build_thopter, weak=False)
        self.group_server = get_group_server()
        pass

    def start_build_thopter(self, sender: NodeSprite):
        Ornithopter(sender.pos, preload=True)
        # make//add _thopter
        pass

    def spawn_thopter(self, sender: NodeSprite):
        # TODO: thechnically more efficient to reassign existing thopter to regular groups
        # instead of removing and adding one.
        unfinished_l = self.group_server.typed_groups["_thopter"].sprites()
        val = unfinished_l[0] if len(unfinished_l) > 0 else None
        if not val:
            raise Exception("finishing construction without ever starting")
        val.kill()
        Ornithopter(sender.pos)
        pass


_instance = None


def get_spawner() -> Spawner:
    global _instance
    if _instance is None:
        _instance = Spawner()  # type: ignore
    return _instance
