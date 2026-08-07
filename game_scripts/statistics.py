import json


class Statistics:
    def __init__(self) -> None:
        with open("statistics.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def __getitem__(self, key):
        return self.data.get(key) or {}


_instance = None


def get_statistics() -> Statistics:
    global _instance
    if _instance is None:
        _instance = Statistics()
    return _instance
