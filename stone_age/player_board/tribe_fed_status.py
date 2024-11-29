from typing import List
from stone_age.interfaces import InterfaceGetState
from stone_age.simple_types import Effect


class TribeFedStatus(InterfaceGetState):
    def __init__(self) -> None:
        self._tribe_fed = False
        self._fields = 0

    def add_field(self) -> None:
        raise NotImplementedError

    def new_turn(self) -> None:
        self._tribe_fed = False

    def feed_tribe_if_enough_food(self) -> bool:
        raise NotImplementedError

    def feed_tribe(self, resources: List[Effect]) -> bool:
        raise NotImplementedError

    def set_tribe_fed(self) -> bool:
        raise NotImplementedError

    def is_tribe_fed(self) -> bool:
        return self._tribe_fed

    @property
    def fields(self) -> int:
        return self._fields

    def state(self) -> str:
        raise NotImplementedError
