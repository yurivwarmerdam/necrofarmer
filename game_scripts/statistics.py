import json
from scripts.group_server import get_group_server


class Statistics:
    def __init__(self) -> None:
        with open("statistics.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def __getitem__(self, key):
        return self.data.get(key) or {}

    @property
    def thopter_cost(self):
        base_cost = self["thopter"]["base_cost"]
        num = get_group_server().get_typed_group_size("Thopter")
        return base_cost * (2**num)

    @property
    def sawmnill_cost(self):
        base_cost = self["sawmill"]["base_cost"]
        num = get_group_server().get_typed_group_size("sawmill")
        return base_cost + (base_cost * num)


_instance = None


def get_statistics() -> Statistics:
    global _instance
    if _instance is None:
        _instance = Statistics()
    return _instance
