from dataclasses import dataclass


@dataclass
class Stockpile:
    wood: int = 500
    stone: int = 20

    def add_wood(self, amount: int):
        self.wood += amount
        print(f"woodamount:{self.wood} {amount}")

    def add_stone(self, amount: int):
        self.stone += amount


_instance: Stockpile | None = None


def get_stockpile() -> Stockpile:
    global _instance
    if _instance is None:
        _instance = Stockpile()
    return _instance
