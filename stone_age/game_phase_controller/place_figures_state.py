from __future__ import annotations
from typing import Mapping
from stone_age.game_phase_controller.interfaces import InterfaceGamePhaseState
from stone_age.interfaces import InterfaceFigureLocation
from stone_age.simple_types import Location, PlayerOrder, ActionResult, HasAction


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
        for place in self._places:
            if self._places[place].try_to_place_figures(player, 1) == HasAction.WAITING_FOR_PLAYER_ACTION:
                return HasAction.WAITING_FOR_PLAYER_ACTION
        return HasAction.NO_ACTION_POSSIBLE
