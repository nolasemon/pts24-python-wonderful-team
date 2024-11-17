import unittest
from stone_age.player_board.player_figures import PlayerFigures


class PlayerFiguresUnit(unittest.TestCase):
    def test_count_figures(self) -> None:
        p1 = PlayerFigures()
        self.assertFalse(p1.take_figures(5))
        self.assertFalse(p1.has_figures(2))
        for _ in range(3):
            p1.add_new_figure()
        self.assertTrue(p1.has_figures(2))
        for _ in range(6):
            p1.add_new_figure()
        self.assertEqual(p1.get_total_figures, 9)
        self.assertTrue(p1.add_new_figure())
        self.assertFalse(p1.add_new_figure())
        self.assertEqual(p1.get_total_figures, 10)

        p2 = PlayerFigures()
        for _ in range(7):
            p2.add_new_figure()
        self.assertEqual(p2.get_total_figures, 7)
        self.assertFalse(p1.add_new_figure())
        self.assertTrue(p2.add_new_figure())
        self.assertEqual(p1.get_total_figures, 10)
        self.assertEqual(p2.get_total_figures, 8)

    def test_run_out_of_figures(self) -> None:
        p1 = PlayerFigures()
        p2 = PlayerFigures()
        p3 = PlayerFigures()
        p4 = PlayerFigures()
        for _ in range(10):
            p1.add_new_figure()
            p2.add_new_figure()
            p3.add_new_figure()
            p4.add_new_figure()
        total_count: int = (p1.get_total_figures + p2.get_total_figures +
                       p3.get_total_figures + p4.get_total_figures)
        self.assertEqual(total_count, 40)
        for _ in range(99):
            p1.add_new_figure()
        self.assertFalse(p2.add_new_figure())
        self.assertGreaterEqual(total_count, 40)

    def test_take_figures(self) -> None:
        p1 = PlayerFigures()
        for _ in range(9):
            p1.add_new_figure()
        self.assertTrue(p1.take_figures(5))
        self.assertEqual(p1.get_total_figures, 9)
        self.assertFalse(p1.take_figures(5))
        self.assertTrue(p1.has_figures(4))
        self.assertTrue(p1.take_figures(4))
        self.assertEqual(p1.get_total_figures, 9)

    def test_state_after_new_turn(self):
        p1 = PlayerFigures()
        for _ in range(7):
            p1.add_new_figure()
        self.assertEqual(p1.get_total_figures, 7)
        self.assertTrue(p1.take_figures(7))
        self.assertEqual(p1.state(), "Actual figures count: 0,\nTotal figures: 7")
        p1.new_turn()
        self.assertEqual(p1.state(), "Actual figures count: 7,\nTotal figures: 7")
        p1.take_figures(3)
        self.assertEqual(p1.state(), "Actual figures count: 4,\nTotal figures: 7")
        p1.new_turn()
        self.assertEqual(p1.state(), "Actual figures count: 4,\nTotal figures: 7")


if __name__ == '__main__':
    unittest.main()
