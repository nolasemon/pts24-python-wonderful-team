import unittest

from stone_age.simple_types import PlayerOrder, Effect
from stone_age.game_board.civilization_card_place import CivilizationCardPlace


class CivilizationCardPlaceTest(unittest.TestCase):
    def test_initial_state(self) -> None:
        place = CivilizationCardPlace(3)
        self.assertEqual(place.required_resources, 3)
        self.assertEqual(place.figures, [])
        self.assertEqual(place.available_cards, [])

    def test_place_figure(self) -> None:
        place = CivilizationCardPlace(3)
        player1 = PlayerOrder(0, 2)
        self.assertTrue(place.place_figure(player1))
        self.assertEqual(place.figures, [player1])
        player2 = PlayerOrder(1, 2)
        self.assertFalse(place.place_figure(player2))
        self.assertEqual(place.figures, [player1])

    def test_remove_figure(self) -> None:
        place = CivilizationCardPlace(3)
        player1 = PlayerOrder(0, 2)
        place.place_figure(player1)
        self.assertTrue(place.remove_figure(player1))
        self.assertEqual(place.figures, [])
        self.assertFalse(place.remove_figure(player1))

    def test_add_card(self) -> None:
        place = CivilizationCardPlace(3)
        card = {"name": "Card 1"}
        place.add_card(card)
        self.assertEqual(place.available_cards, [card])

    def test_acquire_card_no_figure(self) -> None:
        place = CivilizationCardPlace(3)
        card = {"name": "Card 1"}
        place.add_card(card)
        player = PlayerOrder(0, 2)
        self.assertIsNone(place.acquire_card(player, 0))
        self.assertEqual(place.available_cards, [card])

    def test_acquire_card_wrong_player(self) -> None:
        place = CivilizationCardPlace(3)
        card = {"name": "Card 1"}
        place.add_card(card)
        player1 = PlayerOrder(0, 2)
        player2 = PlayerOrder(1, 2)
        place.place_figure(player1)
        self.assertIsNone(place.acquire_card(player2, 0))
        self.assertEqual(place.available_cards, [card])
        self.assertEqual(place.figures, [player1])

    def test_acquire_card_invalid_index(self) -> None:
        place = CivilizationCardPlace(3)
        card = {"name": "Card 1"}
        place.add_card(card)
        player = PlayerOrder(0, 2)
        place.place_figure(player)
        self.assertIsNone(place.acquire_card(player, 1))
        self.assertEqual(place.available_cards, [card])
        self.assertEqual(place.figures, [player])

    def test_acquire_card_success(self) -> None:
        place = CivilizationCardPlace(3)
        card = {"name": "Card 1"}
        place.add_card(card)
        player = PlayerOrder(0, 2)
        place.place_figure(player)
        acquired = place.acquire_card(player, 0)
        self.assertEqual(acquired, card)
        self.assertEqual(place.available_cards, [])
        self.assertEqual(place.figures, [])

    def test_perform_effect_no_figure(self) -> None:
        place = CivilizationCardPlace(3)
        player = PlayerOrder(0, 2)
        self.assertFalse(place.perform_effect(player, Effect.WOOD))

    def test_perform_effect_wrong_player(self) -> None:
        place = CivilizationCardPlace(3)
        player1 = PlayerOrder(0, 2)
        player2 = PlayerOrder(1, 2)
        place.place_figure(player1)
        self.assertFalse(place.perform_effect(player2, Effect.WOOD))

    def test_perform_effect_success(self) -> None:
        place = CivilizationCardPlace(3)
        player1 = PlayerOrder(0, 2)
        place.place_figure(player1)
        self.assertTrue(place.perform_effect(player1, Effect.WOOD))
        self.assertEqual(place.figures, [player1])

    def test_state(self) -> None:
        place = CivilizationCardPlace(3)
        expected_initial_state = ("Civilization Card Place - "
                                  "Required Resources: 3, Figures: [], Cards: []")
        self.assertEqual(place.state(), expected_initial_state)

        card = {"name": "Card 1"}
        place.add_card(card)
        player = PlayerOrder(0, 2)
        place.place_figure(player)
        expected_state_with_card_and_player = (f"Civilization Card Place - "
                                               f"Required Resources: 3, "
                                               f"Figures: {[player]}, Cards: [{card}]")
        self.assertEqual(place.state(), expected_state_with_card_and_player)
