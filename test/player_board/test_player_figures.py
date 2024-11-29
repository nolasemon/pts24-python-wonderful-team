import json
import unittest

from typing import Any
from stone_age.player_board.player_figures import PlayerFigures


class PlayerFiguresUnit(unittest.TestCase):
    def test_count_figures(self) -> None:
        p1 = PlayerFigures()

        # Test that the number of figures for a player is correct
        for _ in range(4):
            p1.add_new_figure()
        self.assertEqual(p1.get_total_figures, 9)
        self.assertTrue(p1.add_new_figure())

        # Player cannot add more figures
        self.assertFalse(p1.add_new_figure())
        self.assertEqual(p1.get_total_figures, 10)

    def test_take_more_figures(self) -> None:
        p1 = PlayerFigures()

        # Tests whether a player is able to take more figures than he actually has
        self.assertFalse(p1.has_figures(7))
        self.assertFalse(p1.take_figures(10))

        for _ in range(5):
            p1.add_new_figure()

        self.assertTrue(p1.has_figures(7))
        self.assertTrue(p1.take_figures(10))
        self.assertFalse(p1.take_figures(2))

    def test_two_players(self) -> None:
        p1 = PlayerFigures()
        p2 = PlayerFigures()

        for _ in range(5):
            p1.add_new_figure()
        for _ in range(2):
            p2.add_new_figure()

        # Test that one player cannot influence another
        self.assertEqual(p2.get_total_figures, 7)
        self.assertFalse(p1.add_new_figure())
        self.assertTrue(p2.add_new_figure())
        self.assertEqual(p1.get_total_figures, 10)
        self.assertEqual(p2.get_total_figures, 8)
        self.assertTrue(p1.take_figures(1))
        self.assertTrue(p2.take_figures(4))

        state1: Any = json.loads(p1.state())
        state2: Any = json.loads(p2.state())

        self.assertEqual(state2, {"figures on player board": 4, "total figures": 8})
        self.assertEqual(state1, {"figures on player board": 9, "total figures": 10})

    def test_run_out_of_figures(self) -> None:
        p1 = PlayerFigures()
        p2 = PlayerFigures()

        for _ in range(5):
            p1.add_new_figure()
            p2.add_new_figure()

        total_count = p1.get_total_figures + p2.get_total_figures

        self.assertEqual(total_count, 20)

        # Test that the players cannot have more than (number of players) * 10 figures
        for _ in range(99):
            p1.add_new_figure()
        self.assertFalse(p2.add_new_figure())
        self.assertEqual(total_count, 20)

    def test_place_figures(self) -> None:
        """Placing figures on the game board does not influence
         the overall number of figures for a player"""

        p1 = PlayerFigures()

        for _ in range(4):
            p1.add_new_figure()

        self.assertTrue(p1.take_figures(5))
        self.assertEqual(p1.get_total_figures, 9)
        self.assertFalse(p1.take_figures(5))
        self.assertTrue(p1.has_figures(4))
        self.assertTrue(p1.take_figures(4))
        self.assertEqual(p1.get_total_figures, 9)

    def test_state_after_new_turn(self) -> None:
        p1 = PlayerFigures()

        for _ in range(2):
            p1.add_new_figure()

        # The number of available figures changes only when there is no figure on the player board
        self.assertEqual(p1.get_total_figures, 7)
        self.assertTrue(p1.take_figures(7))

        state_start: Any = json.loads(p1.state())
        self.assertEqual(state_start, {"figures on player board": 0, "total figures": 7})
        p1.new_turn()
        state_new_turn: Any = json.loads(p1.state())
        self.assertEqual(state_new_turn, {"figures on player board": 7, "total figures": 7})
        p1.take_figures(3)
        state_take_figures: Any = json.loads(p1.state())
        self.assertEqual(state_take_figures, {"figures on player board": 4, "total figures": 7})
        p1.new_turn()
        state_final: Any = json.loads(p1.state())
        self.assertEqual(state_final, {"figures on player board": 4, "total figures": 7})

    def test_negative_count(self) -> None:
        p1 = PlayerFigures()

        # A player cannot take the negative number of figures
        self.assertFalse(p1.take_figures(-1))

        for _ in range(5):
            p1.add_new_figure()

        self.assertFalse(p1.take_figures(11))
        self.assertFalse(p1.take_figures(-1))


if __name__ == '__main__':
    unittest.main()
