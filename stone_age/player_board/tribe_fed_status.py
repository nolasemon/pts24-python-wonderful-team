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
        self._is_food_harvested: bool = False

    @property
    def is_food_harvested(self) -> bool:
        return self._is_food_harvested

    def add_field(self) -> None:
        """Increments `fields` by one if less than `MAX_FIELDS`"""
        if self._fields >= self.MAX_FIELDS:
            return
        self._fields += 1

    def new_turn(self) -> None:
        """Goes to new turn by resetting `tribe_fed` to False"""
        self._tribe_fed = False
        self._is_food_harvested = False
        self._fed_people = 0

    def feed_tribe_if_enough_food(self) -> bool:
        """First stage of feeding.
        Harvests food and if resource_and_food has enough, uses as much food as there are figures

        Returns:
            bool: whether resource_and_food has enough food
        """
        if not self._is_food_harvested:
            self._resources_and_food.give_resources(
                self._fields * [Effect.FOOD])
            self._is_food_harvested = True
        to_feed_count: int = self._figures.get_total_figures - self._fed_people
        necessary_food: List[Effect] = to_feed_count * [Effect.FOOD]
        if not self._resources_and_food.take_resources(necessary_food):
            return False
        self._tribe_fed = True
        return True

    def feed_tribe(self, effects: List[Effect]) -> bool:
        """Second stage of feeding
        Should be called in case if previous stage has failed.
        Feeds tribe with given resources. In case of food shortage will use all food available.

        Args:
            resources (List[Effect]): `resources` if enough to feed will be used entirely,
            whether have excess or not

        Returns:
            bool: whether `resources` is enough
            and `resources_and_food` has `resources`
        """
        while self._fed_people < self._figures.get_total_figures and\
                self._resources_and_food.take_resources([Effect.FOOD]):
            self._fed_people += 1
        remaining: int = self._figures.get_total_figures - self._fed_people
        resources = list(filter(Effect.is_resource, effects))
        if len(resources) < remaining or not self._resources_and_food.take_resources(resources):
            return False
        self._tribe_fed = True
        return True

    def set_tribe_fed(self) -> bool:
        """Last stage of feeding.
        Should be called in case if previous stage has failed.
        Sets `tribe_fed` to True in case of food shortage

        Returns:
            bool: Always True
        """
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
