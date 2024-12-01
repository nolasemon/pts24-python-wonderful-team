import unittest
from typing import List, Iterable
from stone_age.simple_types import ActionResult, CivilisationCard, EndOfGameEffect, PlayerOrder
from stone_age.game_board.simple_types import Player
from stone_age.game_board.civilization_card_deck import CivilizationCardDeck
from stone_age.game_board.get_card import GetCard
from stone_age.interfaces import InterfacePlayerBoardGameBoard


class TestPlayerBoard(InterfacePlayerBoardGameBoard):
    def __init__(self) -> None:
        self.received_effects: List[EndOfGameEffect] = []

    def give_end_of_the_game_effect(self, stuff: Iterable[EndOfGameEffect]) -> None:
        self.received_effects.extend(stuff)


class TestCivilizationCardDeck(CivilizationCardDeck):
    def __init__(self, cards: List[CivilisationCard]) -> None:
        self._cards = cards

    def get_top(self) -> Iterable[CivilisationCard]:
        return [self._cards.pop(0)] if self._cards else []


class TestGetCard(unittest.TestCase):
    def setUp(self) -> None:
        self.player_board = TestPlayerBoard()
        self.player_order = PlayerOrder(order=0, players=2)
        self.player = Player(player_order=self.player_order,
                             player_board=self.player_board)

    def test_perform_effect_with_empty_deck(self) -> None:
        deck = TestCivilizationCardDeck(cards=[])
        get_card = GetCard(deck)

        result = get_card.perform_effect(self.player, choice=[])

        self.assertEqual(result, ActionResult.ACTION_DONE)
        self.assertEqual(len(self.player_board.received_effects), 0)

    def test_perform_effect_with_card_in_deck(self) -> None:
        effect = EndOfGameEffect.FARMER
        card = CivilisationCard(
            immediate_effects=[],
            end_of_game_effects=[effect],
        )
        deck = TestCivilizationCardDeck(cards=[card])
        get_card = GetCard(deck)

        result = get_card.perform_effect(self.player, choice=[])

        self.assertEqual(result, ActionResult.ACTION_DONE)
        self.assertEqual(len(self.player_board.received_effects), 1)
        self.assertIn(effect, self.player_board.received_effects)

    def test_perform_effect_with_multiple_cards_in_deck(self) -> None:
        effect1 = EndOfGameEffect.TOOL_MAKER
        effect2 = EndOfGameEffect.BUILDER
        card1 = CivilisationCard(
            immediate_effects=[],
            end_of_game_effects=[effect1],
        )
        card2 = CivilisationCard(
            immediate_effects=[],
            end_of_game_effects=[effect2],
        )
        deck = TestCivilizationCardDeck(cards=[card1, card2])
        get_card = GetCard(deck)

        result = get_card.perform_effect(self.player, choice=[])
        self.assertEqual(result, ActionResult.ACTION_DONE)
        self.assertEqual(len(self.player_board.received_effects), 1)
        self.assertIn(effect1, self.player_board.received_effects)

        top_card = deck.get_top()
        for card in top_card:
            self.assertEqual(card.end_of_game_effects[0], effect2)


if __name__ == "__main__":
    unittest.main()
