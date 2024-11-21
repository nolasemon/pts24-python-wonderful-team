from __future__ import annotations

from stone_age.game_phase_controller.interfaces import InterfaceGamePhaseState
from stone_age.simple_types import PlayerOrder, HasAction


class GameEndState(InterfaceGamePhaseState):
    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        return HasAction.WAITING_FOR_PLAYER_ACTION

    # other actions should not be done in this phase
