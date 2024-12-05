from typing import Optional, Iterable

from stone_age.player_board.player_board import PlayerBoard, PlayerBoardConfig
from stone_age.interfaces import InterfaceFeedTribe, InterfaceNewTurn, InterfacePlayerBoardGameBoard
from stone_age.simple_types import Effect, EndOfGameEffect


class PlayerBoardGameBoardFacade(InterfacePlayerBoardGameBoard,
                                 InterfaceNewTurn,
                                 InterfaceFeedTribe):

    def __init__(self, player_board_config: PlayerBoardConfig) -> None:
        self._player_board = PlayerBoard(player_board_config)

    @property
    def player_board(self) -> PlayerBoard:
        return self._player_board

    def give_effect(self, stuff: Iterable[Effect]) -> None:
        for item in stuff:
            if Effect.is_resource_or_food(item):
                self._player_board.resources_and_food.give_resources([item])
            elif item == Effect.BUILDING:
                self._player_board.add_house()
            elif item == Effect.FIELD:
                self._player_board.fed_status.add_field()
            elif item == Effect.TOOL:
                self._player_board.tools.add_tool()
            elif item == Effect.POINT:
                self._player_board.add_points(1)
            else:
                strength: int = item - 10  # OneTimeTool2 has a constant value 12 => strength = 2
                self._player_board.tools.add_single_use_tool(strength)

    def give_end_of_the_game_effect(self, stuff: Iterable[EndOfGameEffect]) -> None:
        self._player_board.cards.add_end_of_game_effects(list(stuff))

    def take_resources(self, stuff: Iterable[Effect]) -> bool:
        return self._player_board.resources_and_food.take_resources(list(stuff))

    def take_figures(self, count: int) -> bool:
        return self._player_board.figures.take_figures(count)

    def has_figures(self, count: int) -> bool:
        return self._player_board.figures.has_figures(count)

    def has_sufficient_tools(self, goal: int) -> bool:
        return self._player_board.tools.has_sufficient_tools(goal)

    def use_tool(self, idx: int) -> Optional[int]:
        return self._player_board.tools.use_tool(idx)

    def give_figure(self) -> bool:
        return self._player_board.figures.add_new_figure()

    def feed_tribe_if_enough_food(self) -> bool:
        return self._player_board.fed_status.feed_tribe_if_enough_food()

    def feed_tribe(self, resources: Iterable[Effect]) -> bool:
        return self._player_board.fed_status.feed_tribe(list(resources))

    def do_not_feed_this_turn(self) -> bool:
        assert self._player_board.fed_status.is_food_harvested

        self._player_board.add_points(-10)  # A player loses 10 points
        self.feed_tribe([])
        return self._player_board.fed_status.set_tribe_fed()

    def is_tribe_fed(self) -> bool:
        return self._player_board.fed_status.is_tribe_fed()

    def new_turn(self) -> None:
        self._player_board.fed_status.new_turn()
        self._player_board.figures.new_turn()
        self._player_board.tools.new_turn()
