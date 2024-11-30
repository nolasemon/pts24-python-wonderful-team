from __future__ import annotations
from typing import Iterable
from stone_age.simple_types import Effect, ActionResult
from stone_age.game_board.simple_types import Player
from stone_age.game_board.interfaces import EvaluateCivilizationCardImmediateEffect


class GetChoice(EvaluateCivilizationCardImmediateEffect):
    def __init__(self, number_of_resources: int) -> None:
        self._number_of_resources = number_of_resources

    def perform_effect(self, player: Player, choice: Iterable[Effect]) -> ActionResult:
        if not choice:
            return ActionResult.FAILURE
        if (len(list(choice)) != self._number_of_resources
                or not all(Effect.is_resource(resource) for resource in choice)):
            return ActionResult.FAILURE
        player.player_board.give_effect(list(choice))
        return ActionResult.ACTION_DONE
