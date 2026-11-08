from dataclasses import dataclass


@dataclass
class Stockpile:
    wood: int = 500
    stone: int = 20

    def add_wood(self, amount: int):
        self.wood += amount

    def add_stone(self, amount: int):
        self.stone += amount

    def add_resource(self, amount: list[int]):
        self.wood += amount[0]
        self.stone += amount[1]

    def can_afford(self, amount: list[int]):
        return amount[0] <= self.wood and amount[1] <= self.stone

    def take_resource(self, amount: list[int], partial=False) -> bool | list[int]:
        if self.can_afford(amount):
            self.wood -= amount[0]
            self.stone -= amount[1]
            return True
        else:
            if not partial:
                return False
            wood_taken = min(self.wood, amount[0])
            stone_taken = min(self.stone, amount[1])
            self.wood = max(0, self.wood - amount[0])
            self.stone = max(0, self.wood - amount[1])
            return [wood_taken, stone_taken, 0]

    def can_afford_wood(self, amount) -> bool:
        return amount <= self.wood

    def can_afford_stone(self, amount) -> bool:
        return amount <= self.stone

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
