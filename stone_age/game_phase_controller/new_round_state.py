from __future__ import annotations

from typing import Mapping, Iterable

from stone_age.game_phase_controller.interfaces import GamePhaseStateFailureMeta
from stone_age.interfaces import InterfaceFigureLocation, InterfaceNewTurn
from stone_age.simple_types import PlayerOrder, Location, HasAction, ActionResult, Effect


class NewRoundState(GamePhaseStateFailureMeta):
    """Uses also Mapping[Location, InterfaceFigureLocation], Iterable of
    InterfaceFigureLocation in design makes no sense."""
    _places: Mapping[Location, InterfaceFigureLocation]
    _new_turn: InterfaceNewTurn

    def __init__(self, places: Mapping[Location, InterfaceFigureLocation],
                 new_turn: InterfaceNewTurn):
        self._places = places
        self._new_turn = new_turn

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        """NO_ACTION_POSSIBLE in NEW_ROUND game phase triggers GAME_END."""
        self._new_turn.new_turn()
        for place in self._places:
            if self._places[place].new_turn():
                return HasAction.NO_ACTION_POSSIBLE
        return HasAction.AUTOMATIC_ACTION_DONE

    # other actions should not be done in this phase
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
