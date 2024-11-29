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
        assert False

    def try_to_place_figures(self, player: PlayerOrder, count: int) -> HasAction:
        assert False

    def make_action(self, player: PlayerOrder, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert False

    def skip_action(self, player: PlayerOrder) -> bool:
        assert False

    def try_to_make_action(self, player: PlayerOrder) -> HasAction:
        assert False

    def new_turn(self) -> bool:
        assert False


class InterfacePlayerBoardGameBoard:
    def give_effect(self, stuff: Iterable[Effect]) -> None:
        assert False

    def give_end_of_the_game_effect(self, stuff: Iterable[EndOfGameEffect]) -> None:
        assert False

    def give_figure(self) -> None:
        assert False

    def take_resourses(self, stuff: Iterable[Effect]) -> bool:
        assert False

    def take_figures(self, count: int) -> bool:
        assert False

    def has_figures(self, count: int) -> bool:
        assert False

    def has_sufficient_tools(self, goal: int) -> bool:
        assert False

    def use_tool(self, idx: int) -> Optional[int]:
        assert False


class InterfaceNewTurn:
    def new_turn(self) -> None:
        assert False


class InterfaceToolUse:
    def use_tool(self, idx: int) -> bool:
        assert False

    def can_use_tools(self) -> bool:
        assert False

    def finish_using_tools(self) -> bool:
        assert False


class InterfaceTakeReward:
    def take_reward(self, player: PlayerOrder, reward: Effect) -> bool:
        assert False

    def try_make_action(self, player: PlayerOrder) -> HasAction:
        assert False


class InterfaceFeedTribe:
    def feed_tribe_if_enough_food(self) -> bool:
        assert False

    def feed_tribe(self, resources: Iterable[Effect]) -> bool:
        assert False

    def do_not_feed_this_turn(self) -> bool:
        assert False

    def is_tribe_fed(self) -> bool:
        assert False


class InterfaceStoneAgeGame:
    def place_figures(self, player_id: int, location: Location, figures_count: int) -> bool:
        assert False

    def make_action(self, player_id: int, location: Location,
                    used_resources: Iterable[Effect], desired_resource: Iterable[Effect]) -> bool:
        assert False

    def skip_action(self, player_id: int, location: Location) -> bool:
        assert False

    def use_tools(self, player_id: int, tool_index: int) -> bool:
        assert False

    def no_more_tools_this_throw(self, player_id: int) -> bool:
        assert False

    def feed_tribe(self, player_id: int, resources: Iterable[Effect]) -> bool:
        assert False

    def do_not_feed_this_turn(self, player_id: int) -> bool:
        assert False

    def make_all_players_take_a_reward_choice(self, player_id: int, reward: Effect) -> bool:
        assert False


class InterfaceStoneAgeObserver:
    def update(self, game_state: str) -> None:
        assert False


class InterfaceStoneAgeObservable:
    def register_observer(self, player_id: int, observer: InterfaceStoneAgeObserver) -> None:
        assert False
