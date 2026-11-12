import json
from game_scripts.stockpile import get_stockpile
from scripts.group_server import get_group_server


class Statistics:
    def __init__(self) -> None:
        with open("statistics.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def __getitem__(self, key):
        return self.data.get(key) or {}

    @property
    def thopter_cost(self) -> list[int]:
        base_cost = self["thopter"]["base_cost"]
        num = get_group_server().get_typed_group_size("Thopter")
        return [base_cost[0] * (2**num), 0, 0]

    @property
    def sawmill_cost(self) -> list[int]:
        base_cost = self["sawmill"]["base_cost"]
        num = get_group_server().get_typed_group_size("Sawmill")
        return [base_cost[0] + (base_cost[0] * num), 0, 0]

    def get_cost(self, name: str) -> list[int]:
        return getattr(self, f"{name}_cost")

    def can_afford(self, name: str) -> bool:
        return get_stockpile().can_afford(self.get_cost(name))


_instance = None


def get_statistics() -> Statistics:
    global _instance
    if _instance is None:
        _instance = Statistics()
    return _instance
