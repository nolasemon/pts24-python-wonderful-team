# pylint: disable=unused-argument, duplicate-code
from typing import Iterable, Optional
from stone_age.simple_types import Effect


class Building:
    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        assert False
