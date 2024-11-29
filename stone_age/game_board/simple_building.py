from typing import Iterable, Optional
import json
from stone_age.simple_types import Effect
from stone_age.game_board. interfaces import Building


class SimpleBuilding(Building):
    _required_resources: Iterable[Effect]

    def __init__(self, resources: Iterable[Effect]):
        assert all(Effect.is_resource(x) for x in resources)
        self._required_resources = resources

    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        if not all(Effect.is_resource(x) for x in resources):
            return None
        if sorted(self._required_resources) != sorted(resources):
            return None
        return sum(Effect.points(x) for x in resources)

    @property
    def get_required_resources(self) -> Iterable[Effect]:
        return self._required_resources              # method for testing

    def state(self) -> str:
        d: dict[str, str] = {"Type": "SimpleBuilding",
            "ResourcesRequired" : " ".join(f"{x}" for x in self._required_resources)
                             if self._required_resources else "[]"}
        return json.dumps(d)
