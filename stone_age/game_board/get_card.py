from typing import Optional
from stone_age.simple_types import Effect, CivilisationCard, ActionResult
from stone_age.game_board.interfaces import EvaluateCivilizationCardImmediateEffect
from stone_age.game_board.simple_types import Player
from stone_age.game_board.civilization_card_deck import CivilizationCardDeck

class GetCard(EvaluateCivilizationCardImmediateEffect):
    def __init__(self, card_deck: CivilizationCardDeck):
        self._card_deck = card_deck

    def perform_effect(self, player: Player, choice: Effect) -> ActionResult:
        top_card: Optional[CivilisationCard] = self._card_deck.get_top()
        if top_card is None:
            return ActionResult.ACTION_DONE

        player.player_board.give_end_of_the_game_effect(top_card.end_of_game_effects)
        return ActionResult.ACTION_DONE
