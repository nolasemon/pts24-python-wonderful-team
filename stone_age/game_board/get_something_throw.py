from typing import List
from stone_age.simple_types import Effect


class GetSomethingThrow:
    def __init__(self, resource: List[Effect]):
        self._resource = resource

    @property
    def resource(self) -> List[Effect]:
        return self._resource

    def state(self) -> str:
        return f"Resources to get from throw: {self._resource}"
