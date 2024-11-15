from typing import Iterable, Optional
from stone_age.simple_types import Effect
from stone_age.game_board. interfaces import Building

class VariableBuilding(Building):

    _numberOfResources = int
    _numberOfResourcesTypes = int

    def __init__(self, number_resouces: int, distinct_types: int):
        assert isinstance(number_resouces, int) and isinstance(distinct_types, int)
        self._numberOfResources = number_resouces
        self._numberOfResourceTypes = distinct_types


    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        if not all(Effect.is_resource(x) for x in resources):
            return None
        if len(list(resources)) != self._numberOfResources:
            return None
        if len(set(resources)) != self._numberOfResourceTypes:
            return None
        return sum((Effect.points(x) for x in resources))
