from typing import Iterable, Optional
from stone_age.simple_types import Effect
from stone_age.game_board. interfaces import Building


class VariableBuilding(Building):

    _number_of_resources: int = 0
    _number_of_resources_types: int = 0

    def __init__(self, number_resouces: int, distinct_types: int):
        assert isinstance(number_resouces, int) and isinstance(
            distinct_types, int)
        assert 0 < distinct_types < 5
        self._number_of_resources_types = distinct_types
        self._number_of_resources = number_resouces

    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        if not all(Effect.is_resource(x) for x in resources):
            return None
        if len(list(resources)) != self._number_of_resources:
            return None
        if len(set(resources)) != self._number_of_resources_types:
            return None
        return sum(Effect.points(x) for x in resources)

    @property
    def get_number_of_resources(self) -> int:
        return self._number_of_resources  # method for testing

    @property
    def get_number_of_resources_types(self) -> int:
        return self._number_of_resources_types  # method for testing
