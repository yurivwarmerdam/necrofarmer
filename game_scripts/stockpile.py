from dataclasses import dataclass


@dataclass
class Stockpile:
    wood: int = 0
    stone: int = 0


_instance: Stockpile | None = None


def get_stockpile() -> Stockpile:
    global _instance
    if _instance is None:
        _instance = Stockpile()
    return _instance
