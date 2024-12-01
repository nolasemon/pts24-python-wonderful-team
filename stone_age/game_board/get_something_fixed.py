from typing import Iterable
from stone_age.game_board.simple_types import Player
from stone_age.game_board.interfaces import EvaluateCivilizationCardImmediateEffect
from stone_age.simple_types import Effect, ActionResult


class GetSomethingFixed(EvaluateCivilizationCardImmediateEffect):
    def __init__(self, effect: Effect):
        self._effect = effect

    @property
    def effect(self) -> Effect:
        return self._effect

    def perform_effect(self, player: Player, choice: Iterable[Effect]) -> ActionResult:
        if choice:
            return ActionResult.FAILURE
        player.player_board.give_effect([self.effect])
        return ActionResult.ACTION_DONE

    def state(self) -> str:
        return f"Effects to be applied: {self._effect}"
