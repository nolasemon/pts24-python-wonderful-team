import json
from typing import Iterable, Optional
from stone_age.simple_types import Effect
from stone_age.game_board. interfaces import Building


class ArbitraryBuilding(Building):

    max_number_of_resources: int = 0

    def __init__(self, max_num_resources: int):
        assert isinstance(max_num_resources, int) and max_num_resources > 0
        self.max_number_of_resources = max_num_resources

    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        if not all(Effect.is_resource(x) for x in resources):
            return None
        if len(list(resources)) > self.max_number_of_resources or len(list(resources)) < 1:
            return None
        return sum(Effect.points(x) for x in resources)

    @property
    def get_max_number_of_resources(self) -> int:
        return self.max_number_of_resources  # method for testing

    def state(self) -> str:
        d: dict[str, str] = {"Type": "ArbitraryBuilding",
                        "MaximumResources" : f"{self.max_number_of_resources}"}
        return json.dumps(d)
