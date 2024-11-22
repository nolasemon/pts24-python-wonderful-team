from __future__ import annotations

from typing import Mapping, Iterable

from stone_age.game_phase_controller.interfaces import InterfaceGamePhaseState
from stone_age.interfaces import InterfaceFigureLocation
from stone_age.simple_types import Location, PlayerOrder, ActionResult, HasAction, Effect


class PlaceFiguresState(InterfaceGamePhaseState):
    _places: Mapping[Location, InterfaceFigureLocation]

    def __init__(self, places: Mapping[Location, InterfaceFigureLocation]):
        self._places = places

    def place_figures(self, player: PlayerOrder, location: Location,
                      figures_count: int) -> ActionResult:
        if self._places[location].place_figures(player, figures_count):
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        """
        Automatic placing of figures we do not implement (this could be desirable,
        if all possible locations are occupied, but it is edge case).
        Instead, method checks whether player can place any figures (this should be
        doing self._places[place].try_to_place_figures methods for each location).
        """
        for place in self._places:
            if place == Location.HUT:
                if (self._places[place].try_to_place_figures(player, 2)
                        == HasAction.WAITING_FOR_PLAYER_ACTION):
                    return HasAction.WAITING_FOR_PLAYER_ACTION
            elif (self._places[place].try_to_place_figures(player, 1)
                  == HasAction.WAITING_FOR_PLAYER_ACTION):
                return HasAction.WAITING_FOR_PLAYER_ACTION
        return HasAction.NO_ACTION_POSSIBLE

    # other actions should not be done in this phase
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
