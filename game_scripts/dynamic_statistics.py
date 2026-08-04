from game_scripts.statistics import get_statistics
from group_server import get_group_server


class DynamicStatistics:
    def __init__(self) -> None:
        self.statistics = get_statistics()
        self.group_server = get_group_server()

    @property
    def thopter_cost(self):
        base_cost = self.statistics["thopter"]["base_cost"]
        num_thopters = self.group_server.get_typed_group_size("Thopter")
        return base_cost * (2**num_thopters)


_instance = None


def get_dynamic_statistics() -> DynamicStatistics:
    global _instance
    if _instance is None:
        _instance = DynamicStatistics()
    return _instance
