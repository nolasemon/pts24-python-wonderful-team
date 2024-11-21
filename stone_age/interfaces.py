# pylint: disable=unused-argument, duplicate-code
from __future__ import annotations
from typing import Iterable, Optional
from stone_age.simple_types import PlayerOrder, Location, Effect
from stone_age.simple_types import HasAction, ActionResult, EndOfGameEffect


class InterfaceGamePhaseController:
    def place_figures(self, player: PlayerOrder, location: Location, figures_count: int) -> bool:
        assert False

    def make_action(self, player: PlayerOrder, location: Location,
                    input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> bool:
        assert False

    def skip_action(self, player: PlayerOrder, location: Location) -> bool:
        assert False

    def use_tools(self, player: PlayerOrder, tool_index: int) -> bool:
        assert False

    def no_more_tools_this_throw(self, player: PlayerOrder) -> bool:
        assert False

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> bool:
        assert False

    def do_not_feed_this_turn(self, player: PlayerOrder) -> bool:
        assert False

    def make_all_players_take_a_reward_choice(self, player: PlayerOrder, reward: Effect) -> bool:
        assert False

    def state(self) -> str:
        assert False


class InterfaceGetState:
    def get_state(self) -> str:
        assert False


class InterfaceFigureLocation:

    def place_figures(self, player: PlayerOrder, figure_count: int) -> bool:
        assert isinstance(player, PlayerOrder) and figure_count > 0
        return False

    def try_to_place_figures(self, player: PlayerOrder, count: int) -> HasAction:
        assert isinstance(player, PlayerOrder) and count > 0
        return HasAction.NO_ACTION_POSSIBLE

    def make_action(self, player: PlayerOrder, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        assert isinstance(input_resources, Iterable) and isinstance(
            output_resources, Iterable)
        return ActionResult.FAILURE

    def skip_action(self, player: PlayerOrder) -> bool:
        assert isinstance(player, PlayerOrder)
        return False

    def try_to_make_action(self, player: PlayerOrder) -> HasAction:
        assert isinstance(player, PlayerOrder)
        return HasAction.NO_ACTION_POSSIBLE

    def new_turn(self) -> bool:
        return False


class InterfacePlayerBoardGameBoard:

    def give_effect(self, stuff: Iterable[Effect]) -> None:
        assert all(isinstance(effect, Effect) for effect in stuff)

    def give_end_of_the_game_effect(self, stuff: Iterable[EndOfGameEffect]) -> None:
        assert all(isinstance(effect, EndOfGameEffect) for effect in stuff)

    def give_figure(self) -> None:
        pass

    def take_resourses(self, stuff: Iterable[Effect]) -> bool:
        assert all(isinstance(effect, Effect) for effect in stuff)
        return False

    def take_figures(self, count: int) -> bool:
        assert isinstance(count, int)
        return False

    def has_figures(self, count: int) -> bool:
        assert isinstance(count, int)
        return False

    def has_sufficient_tools(self, goal: int) -> bool:
        assert isinstance(goal, int)
        return False

    def use_tool(self, idx: int) -> Optional[int]:
        assert isinstance(idx, int)
        return 0


class InterfaceNewTurn:
    def new_turn(self) -> None:
        assert False
