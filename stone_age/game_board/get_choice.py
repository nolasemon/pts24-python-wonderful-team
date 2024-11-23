from typing import List, Dict
from collections import Counter
from stone_age.simple_types import Effect


class GetChoice:
    def __init__(self, number_of_resources: List[Effect]):
        self._number_of_resources_count = dict(Counter(number_of_resources))
        self._chosen_resources: Dict[Effect, int] = {}

    @property
    def number_of_resources(self) -> Dict[Effect, int]:
        return self._number_of_resources_count

    @property
    def chosen_resources(self) -> Dict[Effect, int]:
        return self._chosen_resources

    def make_choice(self, choice: Dict[Effect, int]) -> bool:
        for resource, count in choice.items():
            if (resource not in self._number_of_resources_count
                    or count > self._number_of_resources_count[resource]):
                return False
        self._chosen_resources = choice
        return True

    def state(self) -> str:
        return (f"Number of resources to choose from: {self._number_of_resources_count}, "
                f"Chosen resources: {self._chosen_resources}")
