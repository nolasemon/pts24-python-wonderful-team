from typing import List
from random import randint


class Throw:

    minNumber: int = 1
    maxNumber: int = 6

    def throw(self, dices: int) -> List[int]:
        assert isinstance(dices, int) and dices > 0
        results: List[int] = [
            randint(self.minNumber, self.maxNumber) for dice in range(dices)]
        return results
