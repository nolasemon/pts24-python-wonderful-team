import unittest
from stone_age.simple_types import EndOfGameEffect
from stone_age.player_board.player_civilisation_cards import PlayerCivilisationCards

class TestPlayerCivilisationCards(unittest.TestCase):
    def setUp(self) -> None:
        self.cards = PlayerCivilisationCards()

    def test_empty_cards_zero_points(self) -> None:
        points = self.cards.calculate_end_of_game_civilisation_card_points(0, 0, 0, 0)
        self.assertEqual(points, 0)

    def test_sand_background_cards_scoring(self) -> None:
        # Test case from rules: 5 farmers x 7 agriculture = 35 points
        self.cards.add_end_of_game_effects([EndOfGameEffect.FARMER] * 5)
        points = self.cards.calculate_end_of_game_civilisation_card_points(0, 0, 7, 0)
        self.assertEqual(points, 35)

        # Test case from rules: 3 tool makers x 7 tool value = 21 points
        self.cards = PlayerCivilisationCards()
        self.cards.add_end_of_game_effects([EndOfGameEffect.TOOL_MAKER] * 3)
        points = self.cards.calculate_end_of_game_civilisation_card_points(0, 7, 0, 0)
        self.assertEqual(points, 21)

        # Test case from rules: 7 builders x 6 buildings = 42 points
        self.cards = PlayerCivilisationCards()
        self.cards.add_end_of_game_effects([EndOfGameEffect.BUILDER] * 7)
        points = self.cards.calculate_end_of_game_civilisation_card_points(6, 0, 0, 0)
        self.assertEqual(points, 42)

        # Test case from rules: 3 shamans x 8 figures = 24 points
        self.cards = PlayerCivilisationCards()
        self.cards.add_end_of_game_effects([EndOfGameEffect.SHAMAN] * 3)
        points = self.cards.calculate_end_of_game_civilisation_card_points(0, 0, 0, 8)
        self.assertEqual(points, 24)

    def test_green_background_cards_scoring(self) -> None:
        # Test single set of 5 different cards: 5x5 = 25 points
        green_cards = [
            EndOfGameEffect.ART,
            EndOfGameEffect.MEDICINE,
            EndOfGameEffect.MUSIC,
            EndOfGameEffect.POTTERY,
            EndOfGameEffect.SUNDIAL
        ]
        self.cards.add_end_of_game_effects(green_cards)
        points = self.cards.calculate_end_of_game_civilisation_card_points(0, 0, 0, 0)
        self.assertEqual(points, 25)

        # Test multiple sets with duplicate cards
        self.cards = PlayerCivilisationCards()
        green_cards = [
            EndOfGameEffect.ART,
            EndOfGameEffect.MEDICINE,
            EndOfGameEffect.MUSIC,
            EndOfGameEffect.ART,
            EndOfGameEffect.MEDICINE
        ]
        self.cards.add_end_of_game_effects(green_cards)
        points = self.cards.calculate_end_of_game_civilisation_card_points(0, 0, 0, 0)
        self.assertEqual(points, 13)

        self.cards = PlayerCivilisationCards()
        green_cards = [
            EndOfGameEffect.ART,
            EndOfGameEffect.MEDICINE,
            EndOfGameEffect.MUSIC,
            EndOfGameEffect.POTTERY,
            EndOfGameEffect.SUNDIAL,
            EndOfGameEffect.POTTERY
        ]
        self.cards.add_end_of_game_effects(green_cards)
        points = self.cards.calculate_end_of_game_civilisation_card_points(0, 0, 0, 0)
        self.assertEqual(points, 26)

    def test_combined_scoring(self) -> None:
        # Test combination of sand and green cards
        self.cards.add_end_of_game_effects([
            EndOfGameEffect.FARMER,
            EndOfGameEffect.ART,
            EndOfGameEffect.MEDICINE,
            EndOfGameEffect.MUSIC 
        ])
        points = self.cards.calculate_end_of_game_civilisation_card_points(0, 0, 5, 0)
        self.assertEqual(points, 14)

    def test_state_representation(self) -> None:
        self.cards.add_end_of_game_effects([EndOfGameEffect.FARMER, EndOfGameEffect.FARMER])
        state = self.cards.state()
        self.assertIn("FARMER", state)
        self.assertIn("2", state)

if __name__ == "__main__":
    unittest.main()