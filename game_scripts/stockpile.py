from dataclasses import dataclass


@dataclass
class Stockpile:
    wood: int = 500
    stone: int = 20

    def add_wood(self, amount: int):
        self.wood += amount

    def add_stone(self, amount: int):
        self.stone += amount

    def can_afford_wood(self, amount) -> bool:
        return amount >= self.wood

    def can_afford_stone(self, amount) -> bool:
        return amount >= self.stone

    def take_wood(self, amount, partial=False) -> int | bool:
        if partial:
            if self.wood < amount:
                buf = self.wood
                self.wood = 0
                return buf
            else:
                self.wood -= amount
                return amount
        else:
            if self.wood < amount:
                return False
            else:
                self.wood -= amount
                return True

    def take_stone(self, amount, partial=False) -> int | bool:
        if partial:
            if self.stone < amount:
                buf = self.stone
                self.stone = 0
                return buf
            else:
                self.stone -= amount
                return amount
        else:
            if self.stone < amount:
                return False
            else:
                self.stone -= amount
                return True


_instance: Stockpile | None = None


def get_stockpile() -> Stockpile:
    global _instance
    if _instance is None:
        _instance = Stockpile()
    return _instance
