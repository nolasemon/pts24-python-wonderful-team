from player_board import PlayerBoard, PlayerBoardConfig
from typing import Optional, List

from stone_age.interfaces import InterfaceFeedTribe, InterfaceNewTurn, InterfacePlayerBoardGameBoard
from stone_age.simple_types import Effect, EndOfGameEffect


class PlayerBoardGameBoardFacade(InterfacePlayerBoardGameBoard, InterfaceNewTurn, InterfaceFeedTribe):

    def __init__(self, player_board_config: PlayerBoardConfig) -> None:
        assert isinstance(player_board_config, PlayerBoardConfig)

        self._player_board = PlayerBoard(player_board_config)

    @property
    def player_board(self) -> PlayerBoard:
        return self._player_board

    def give_effect(self, stuff: List[Effect]) -> None:
        assert all(isinstance(item, Effect) for item in stuff)

        resources_and_food: List[Effect] = []

        for item in stuff:
            if Effect.is_resource_or_food(item):
                resources_and_food.append(item)
            elif item == Effect.BUILDING:
                self._player_board.add_house()
            elif item == Effect.FIELD:
                self._player_board._fed_status.add_field()
            else:
                self._player_board._tools.add_single_use_tool(item - 10)

        self._player_board._resources_and_food.take_resources(resources_and_food)

    def give_end_of_the_game_effect(self, stuff: List[EndOfGameEffect]) -> None:
        assert all(isinstance(item, Effect) for item in stuff)

        self._player_board._cards.add_end_of_game_effects(stuff)

    def take_resourses(self, stuff: List[Effect]) -> bool:
        assert all(isinstance(effect, Effect) for effect in stuff)

        return self._player_board._resources_and_food.take_resources(stuff)

    def take_figures(self, count: int) -> bool:
        assert count > 0

        return self._player_board._figures.take_figures(count)

    def has_figures(self, count: int) -> bool:
        assert count > 0

        return self._player_board._figures.has_figures(count)

    def has_sufficient_tools(self, goal: int) -> bool:
        assert goal > 0

        return self._player_board._tools.has_sufficient_tools(goal)

    def use_tool(self, idx: int) -> Optional[int]:
        assert idx > 0

        self._player_board._tools.use_tool(idx)

    def give_figure(self) -> bool:
        return self._player_board._figures.add_new_figure()

    def feed_tribe_if_enough_food(self) -> bool:
        return self._player_board._fed_status.feed_tribe_if_enough_food()

    def feed_tribe(self, resources: List[Effect]) -> bool:
        assert all(isinstance(resource, Effect) for resource in resources)

        return self._player_board._fed_status.feed_tribe(resources)

    def do_not_feed_this_turn(self) -> bool:
        return self.is_tribe_fed()

    def is_tribe_fed(self) -> bool:
        return self._player_board._fed_status.is_tribe_fed()

    def new_turn(self) -> None:
        self._player_board._fed_status.new_turn()
        self._player_board._figures.new_turn()
        self._player_board._tools.new_turn()
