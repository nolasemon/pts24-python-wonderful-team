from collections import defaultdict
from typing import Any
import json

from stone_age.interfaces import InterfaceGetState
from stone_age.simple_types import Effect


class PlayerResourcesAndFood(InterfaceGetState):

    def __init__(self) -> None:
        self._resources: dict[Effect, int] = defaultdict(int)

    def has_resources(self, resources: list[Effect]) -> bool:
        resource_counts: dict[Effect, int] = {}
        for resource in resources:
            resource_counts[resource] = resource_counts.get(resource, 0) + 1
            if self._resources[resource] < resource_counts[resource]:
                return False
        return True

    def give_resources(self, resources: list[Effect]) -> bool:
        """Add resources to player's inventory"""
        for resource in resources:
            self._resources[resource] += 1
        return True

    def take_resources(self, resources: list[Effect]) -> bool:
        """Remove resources from player's inventory if possible"""
        if not self.has_resources(resources):
            return False

        for resource in resources:
            self._resources[resource] = max(self._resources[resource] - 1, 0)
        return True

    def number_of_resources_for_final_points(self) -> int:
        """Calculate final points from resources"""
        return sum(Effect.points(resource) * count
                   for resource, count in self._resources.items())

    def state(self) -> str:
        state: Any = {
            entry.name: self._resources.get(entry, 0)
            for entry in Effect
            if Effect.is_resource_or_food(entry)
        }
        return json.dumps(state)
