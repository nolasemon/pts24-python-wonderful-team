from __future__ import annotations

from typing import Mapping

from stone_age.game_phase_controller.interfaces import InterfaceGamePhaseState
from stone_age.interfaces import InterfaceFigureLocation, InterfaceNewTurn
from stone_age.simple_types import PlayerOrder, Location, HasAction


class NewRoundState(InterfaceGamePhaseState):
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
        for place in self._places:
            if self._places[place].new_turn():
                return HasAction.NO_ACTION_POSSIBLE
        self._new_turn.new_turn()
        return HasAction.AUTOMATIC_ACTION_DONE

    # other actions should not be done in this phase
