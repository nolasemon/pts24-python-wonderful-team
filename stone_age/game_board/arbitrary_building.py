from typing import Iterable, Optional
from stone_age.simple_types import Effect
from stone_age.game_board. interfaces import Building

class ArbitraryBuilding(Building):

    maxNumberOfResources: Optional[int] = None

    def __init__(self, max_num_resources: int):
        assert isinstance(max_num_resources, int) and max_num_resources > 0
        self.maxNumberOfResources = max_num_resources

    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        if not all(Effect.is_resource(x) for x in resources):
            return None
        if len(list(resources)) > self.maxNumberOfResources or len(list(resources)) < 1:
            return None
        return sum((Effect.points(x) for x in resources))

    @property
    def get_maxNumberOfResources(self) -> int:
        return self.maxNumberOfResources               #method for testing