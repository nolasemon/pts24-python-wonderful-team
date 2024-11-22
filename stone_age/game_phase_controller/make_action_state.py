from __future__ import annotations

from typing import Iterable, Mapping

from stone_age.game_phase_controller.interfaces import InterfaceGamePhaseState
from stone_age.interfaces import InterfaceFigureLocation
from stone_age.simple_types import PlayerOrder, Location, Effect, ActionResult, HasAction


class MakeActionState(InterfaceGamePhaseState):
    _places: Mapping[Location, InterfaceFigureLocation]

    def __init__(self, places: Mapping[Location, InterfaceFigureLocation]):
        self._places = places

    def make_action(self, player: PlayerOrder, location: Location,
                    input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        return self._places[location].make_action(player, input_resources, output_resources)

    def skip_action(self, player: PlayerOrder, location: Location) -> ActionResult:
        """Converts bool output from InterfaceFigureLocation into ActionResult."""
        if self._places[location].skip_action(player):
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        """If automatic action can be done, self._places[place].try_to_make_action
        should do it, otherwise returns whether there are some figures on player board
        waiting for player to make action."""
        waiting: bool = False
        for place in self._places:
            try_output: HasAction = self._places[place].try_to_make_action(
                player)
            if try_output == HasAction.AUTOMATIC_ACTION_DONE:
                return HasAction.AUTOMATIC_ACTION_DONE
            if try_output == HasAction.WAITING_FOR_PLAYER_ACTION:
                waiting = True
        return HasAction.WAITING_FOR_PLAYER_ACTION if waiting else HasAction.NO_ACTION_POSSIBLE

    # other actions should not be done in this phase
    def place_figures(self, player: PlayerOrder, location: Location,
                      figures_count: int) -> ActionResult:
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
