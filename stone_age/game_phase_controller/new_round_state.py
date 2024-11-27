from __future__ import annotations

from typing import Mapping

from stone_age.game_phase_controller.interfaces import GamePhaseStateFailureMeta
from stone_age.interfaces import InterfaceFigureLocation, InterfaceNewTurn
from stone_age.simple_types import PlayerOrder, Location, HasAction


class NewRoundState(GamePhaseStateFailureMeta):
    """
    Uses also Mapping[Location, InterfaceFigureLocation], Iterable of
    InterfaceFigureLocation in design makes no sense.
    Second argument in constructor is needed for new_turn method call
    for each of the player boards.
    """
    _places: Mapping[Location, InterfaceFigureLocation]
    _new_turn: Mapping[PlayerOrder, InterfaceNewTurn]

    def __init__(self, places: Mapping[Location, InterfaceFigureLocation],
                 new_turn: Mapping[PlayerOrder, InterfaceNewTurn]):
        self._places = places
        self._new_turn = new_turn

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        """NO_ACTION_POSSIBLE in NEW_ROUND game phase triggers GAME_END."""
        for player_board in self._new_turn:
            self._new_turn[player_board].new_turn()
        for place in sorted(self._places.keys()):
            if self._places[place].new_turn():
                return HasAction.NO_ACTION_POSSIBLE
        return HasAction.AUTOMATIC_ACTION_DONE

    # other actions should not be done in this phase
