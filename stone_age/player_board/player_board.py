from dataclasses import dataclass
from typing import Any, override
import json
from stone_age.interfaces import InterfaceGetState
from stone_age.player_board.player_civilisation_cards import PlayerCivilisationCards
from stone_age.player_board.player_tools import PlayerTools
from stone_age.player_board.player_resources_and_food import PlayerResourcesAndFood
from stone_age.player_board.tribe_fed_status import TribeFedStatus
from stone_age.player_board.player_figures import PlayerFigures


@dataclass
class PlayerBoardConfig:
    points: int
    houses: int
    cards: PlayerCivilisationCards
    tools: PlayerTools
    resources_and_food: PlayerResourcesAndFood
    fed_status: TribeFedStatus
    figures: PlayerFigures


class PlayerBoard(InterfaceGetState):
    def __init__(self, config: PlayerBoardConfig) -> None:
        self._points = config.points
        self._houses = config.houses
        self._cards = config.cards
        self._resources_and_food = config.resources_and_food
        self._fed_status = config.fed_status
        self._figures = config.figures
        self._tools = config.tools

    @property
    def cards(self) -> PlayerCivilisationCards:
        return self._cards

    @property
    def resources_and_food(self) -> PlayerResourcesAndFood:
        return self._resources_and_food

    @property
    def fed_status(self) -> TribeFedStatus:
        return self._fed_status

    @property
    def figures(self) -> PlayerFigures:
        return self._figures

    @property
    def tools(self) -> PlayerTools:
        return self._tools

    def add_points(self, points: int) -> None:
        self._points += points

    def add_house(self) -> None:
        self._houses += 1

    def add_end_of_game_points(self) -> None:
        self._points += self._resources_and_food.number_of_resources_for_final_points()
        self._points += self._cards.calculate_end_of_game_civilisation_card_points(
            self._houses,
            self._tools.tool_count,
            self._fed_status.fields,
            self._figures.get_total_figures
        )

    @override
    def state(self) -> str:
        state: Any = {
            "points": self._points,
            "houses": self._houses,
            "civilisation cards": self._cards.state(),
            "tools": self._tools.state(),
            "resources and food": self._resources_and_food.state(),
            "tribe fed status": self._fed_status.state(),
            "figures": self._figures.state()
        }
        return json.dumps(state)
