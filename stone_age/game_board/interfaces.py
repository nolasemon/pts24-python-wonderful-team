# pylint: disable=unused-argument, duplicate-code
from typing import Iterable, Optional
from stone_age.simple_types import Effect


class Building:

    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        assert all(Effect.is_resource(x) for x in resources)
        return sum(Effect.points(x) for x in resources)
