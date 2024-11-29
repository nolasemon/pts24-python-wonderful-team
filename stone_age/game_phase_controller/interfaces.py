# pylint: disable=unused-argument, duplicate-code
from __future__ import annotations
from typing import Iterable
from stone_age.simple_types import PlayerOrder, Location, Effect
from stone_age.simple_types import HasAction, ActionResult


class InterfaceGamePhaseState:
    def place_figures(self, player: PlayerOrder, location: Location,
                      figures_count: int) -> ActionResult:
        assert False

    def make_action(self, player: PlayerOrder, location: Location,
                    input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert False

    def skip_action(self, player: PlayerOrder, location: Location) -> ActionResult:
        assert False

    def use_tools(self, player: PlayerOrder, tool_index: int) -> ActionResult:
        assert False

    def no_more_tools_this_throw(self, player: PlayerOrder) -> ActionResult:
        assert False

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> ActionResult:
        assert False

    def do_not_feed_this_turn(self, player: PlayerOrder) -> ActionResult:
        assert False

    def make_all_players_take_a_reward_choice(self, player: PlayerOrder,
                                              reward: Effect) -> ActionResult:
        assert False

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        assert False


class GamePhaseStateFailureMeta(InterfaceGamePhaseState):
    """
    Created for game phase classes to give them methods returning ActionResult.FAILURE
    without need to redefine all these methods.
    """

    def place_figures(self, player: PlayerOrder, location: Location,
                      figures_count: int) -> ActionResult:
        return ActionResult.FAILURE

    def make_action(self, player: PlayerOrder, location: Location,
                    input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        return ActionResult.FAILURE

    def skip_action(self, player: PlayerOrder, location: Location) -> ActionResult:
        return ActionResult.FAILURE

    def use_tools(self, player: PlayerOrder, tool_index: int) -> ActionResult:
        return ActionResult.FAILURE

    def no_more_tools_this_throw(self, player: PlayerOrder) -> ActionResult:
        return ActionResult.FAILURE

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> ActionResult:
        return ActionResult.FAILURE

    def do_not_feed_this_turn(self, player: PlayerOrder) -> ActionResult:
        return ActionResult.FAILURE

    def make_all_players_take_a_reward_choice(self, player: PlayerOrder,
                                              reward: Effect) -> ActionResult:
        return ActionResult.FAILURE

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        assert False
