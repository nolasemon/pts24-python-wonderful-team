from typing import List, Any
import json

from stone_age.interfaces import InterfaceGetState
from stone_age.simple_types import Effect
from stone_age.player_board.player_resources_and_food import PlayerResourcesAndFood
from stone_age.player_board.player_figures import PlayerFigures


class TribeFedStatus(InterfaceGetState):
    MAX_FIELDS: int = 11

    def __init__(
        self,
        resources_and_food: PlayerResourcesAndFood,
        figures: PlayerFigures
    ) -> None:
        self._tribe_fed: bool = False
        self._fields: int = 0
        self._resources_and_food: PlayerResourcesAndFood = resources_and_food
        self._figures: PlayerFigures = figures
        # suppose feed methods can be called more than once in a round
        self._fed_people: int = 0
        self._new_fields: int = 0

    def add_field(self) -> None:
        if self._fields >= self.MAX_FIELDS:
            return
        self._fields += 1
        self._new_fields += 1

    def new_turn(self) -> None:
        self._tribe_fed = False
        self._new_fields = 0
        self._fed_people = 0

    def feed_tribe_if_enough_food(self) -> bool:
        self._resources_and_food.take_resources(
            self._new_fields * [Effect.FOOD])
        self._new_fields = 0
        to_feed_count: int = self._figures.get_total_figures - self._fed_people
        necessary_food: List[Effect] = to_feed_count * [Effect.FOOD]
        if not self._resources_and_food.has_resources(necessary_food):
            return False
        self._tribe_fed = True
        self._resources_and_food.give_resources(necessary_food)
        return True

    def feed_tribe(self, resources: List[Effect]) -> bool:
        while self._fed_people < self._figures.get_total_figures and\
                self._resources_and_food.has_resources([Effect.FOOD]):
            self._fed_people += 1
            self._resources_and_food.give_resources([Effect.FOOD])
        remaining: int = self._figures.get_total_figures - self._fed_people
        if len(resources) < remaining or not self._resources_and_food.has_resources(resources):
            return False
        self._resources_and_food.give_resources(resources)
        self._tribe_fed = True
        return True

    def set_tribe_fed(self) -> bool:
        self._tribe_fed = True
        return True

    def is_tribe_fed(self) -> bool:
        return self._tribe_fed

    @property
    def fields(self) -> int:
        return self._fields

    def state(self) -> str:
        state: Any = {
            "tribe fed": self._tribe_fed,
            "fields": self._fields,
        }
        return json.dumps(state)
