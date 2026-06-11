from dataclasses import dataclass


@dataclass
class Stockpile:
    wood: int = 500
    stone: int = 20


_instance: Stockpile | None = None


def get_stockpile() -> Stockpile:
    global _instance
    if _instance is None:
        _instance = Stockpile()
    return _instance
