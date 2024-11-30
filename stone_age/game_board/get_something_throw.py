from __future__ import annotations
from typing import Iterable
from stone_age.simple_types import Effect, ActionResult
from stone_age.game_board.simple_types import Player
from stone_age.game_board.interfaces import EvaluateCivilizationCardImmediateEffect
from stone_age.game_board.interfaces import InterfaceCurrentThrow


class GetSomethingThrow(EvaluateCivilizationCardImmediateEffect):
    def __init__(self, current_throw: InterfaceCurrentThrow, resource: Effect) -> None:
        self._current_throw = current_throw
        self._resource = resource

    def perform_effect(self, player: Player, choice: Iterable[Effect] = ()) -> ActionResult:
        self._current_throw.initiate(player, self._resource, 2)
        return ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE
