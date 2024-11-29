import unittest
from stone_age.player_board.player_tools import PlayerTools


class TestPlayerTools(unittest.TestCase):

    def test_tools_adding(self) -> None:
        p1 = PlayerTools()

        p1.add_tool()
        p1.add_tool()

        self.assertIn("Tool 1: 1, unused\nTool 2: 1, unused", p1.state())
        self.assertFalse(p1.has_sufficient_tools(11))

        for _ in range(4):
            p1.add_tool()

        self.assertIn(
            "Tool 1: 2, unused\nTool 2: 2, unused\nTool 3: 2, unused", p1.state())
        self.assertFalse(p1.has_sufficient_tools(11))

        for _ in range(4):
            p1.add_tool()

        self.assertIn(
            "Tool 1: 4, unused\nTool 2: 3, unused\nTool 3: 3, unused", p1.state())
        self.assertFalse(p1.has_sufficient_tools(11))

        for _ in range(3):
            p1.add_tool()

        self.assertIn(
            "Tool 1: 4, unused\nTool 2: 4, unused\nTool 3: 4, unused", p1.state())
        self.assertTrue(p1.has_sufficient_tools(11))

    def test_figures_taking(self) -> None:
        p1 = PlayerTools()

        for _ in range(10):
            p1.add_tool()

        self.assertTrue(p1.has_sufficient_tools(7))
        p1.use_tool(0)
        self.assertFalse(p1.has_sufficient_tools(7))
        self.assertIn(
            "Tool 1: 4, used\nTool 2: 3, unused\nTool 3: 3, unused", p1.state())
        p1.use_tool(1)
        p1.use_tool(2)
        self.assertIn(
            "Tool 1: 4, used\nTool 2: 3, used\nTool 3: 3, used", p1.state())
        p1.add_tool()
        self.assertIn(
            "Tool 1: 4, used\nTool 2: 4, used\nTool 3: 3, used", p1.state())
        self.assertFalse(p1.has_sufficient_tools(4))

    def test_new_turn(self) -> None:
        p1 = PlayerTools()

        for _ in range(10):
            p1.add_tool()

        p1.use_tool(0)
        p1.use_tool(1)
        self.assertIn(
            "Tool 1: 4, used\nTool 2: 3, used\nTool 3: 3, unused", p1.state())
        p1.new_turn()
        self.assertIn(
            "Tool 1: 4, unused\nTool 2: 3, unused\nTool 3: 3, unused", p1.state())

    def test_single_use_tool(self) -> None:
        p1 = PlayerTools()

        p1.add_single_use_tool(3)
        self.assertIn("Single-use tool: 3, unused", p1.state())
        p1.add_tool()
        p1.add_tool()
        self.assertIn("Tool 1: 1, unused\nTool 2: 1, unused\n"
                      "Single-use tool: 3, unused", p1.state())
        p1.add_single_use_tool(2)
        self.assertIn("Tool 1: 1, unused\nTool 2: 1, unused\n"
                      "Single-use tool: 3, unused\nSingle-use tool: 2, unused", p1.state())
        self.assertTrue(p1.has_sufficient_tools(5))
        p1.use_tool(3)
        self.assertIn("Tool 1: 1, unused\nTool 2: 1, unused\n"
                      "Single-use tool: 2, unused", p1.state())
        self.assertFalse(p1.has_sufficient_tools(5))
        p1.add_tool()
        self.assertIn("Tool 1: 1, unused\nTool 2: 1, unused\n"
                      "Tool 3: 1, unused\nSingle-use tool: 2, unused", p1.state())
        p1.new_turn()
        self.assertIn("Tool 1: 1, unused\nTool 2: 1, unused\n"
                      "Tool 3: 1, unused\nSingle-use tool: 2, unused", p1.state())
        p1.add_single_use_tool(1)
        p1.add_single_use_tool(5)
        p1.add_single_use_tool(-1)
        self.assertIn("Tool 1: 1, unused\nTool 2: 1, unused\n"
                      "Tool 3: 1, unused\nSingle-use tool: 2, unused", p1.state())

    def test_add_too_much(self) -> None:
        p1 = PlayerTools()

        for _ in range(100):
            p1.add_tool()

        self.assertIn(
            "Tool 1: 4, unused\nTool 2: 4, unused\nTool 3: 4, unused", p1.state())
        p1.add_single_use_tool(2)
        p1.add_single_use_tool(3)
        p1.add_single_use_tool(4)
        self.assertIn("Tool 1: 4, unused\nTool 2: 4, unused\nTool 3: 4, unused\n"
                      "Single-use tool: 2, unused\nSingle-use tool: 3, unused\n"
                      "Single-use tool: 4, unused", p1.state())
        p1.add_tool()
        p1.add_tool()
        p1.add_single_use_tool(2)
        self.assertIn("Tool 1: 4, unused\nTool 2: 4, unused\nTool 3: 4, unused\n"
                      "Single-use tool: 2, unused\nSingle-use tool: 3, unused\n"
                      "Single-use tool: 4, unused\nSingle-use tool: 2, unused", p1.state())
        p1.use_tool(4)
        p1.use_tool(5)
        self.assertIn("Tool 1: 4, unused\nTool 2: 4, unused\nTool 3: 4, unused\n"
                      "Single-use tool: 2, unused\nSingle-use tool: 4, unused", p1.state())

    def test_use_tools(self) -> None:
        p1 = PlayerTools()

        self.assertEqual(p1.use_tool(-1), None)
        self.assertEqual(p1.use_tool(3), None)
        p1.add_tool()
        p1.add_tool()
        self.assertEqual(p1.use_tool(0), 1)
        self.assertEqual(p1.use_tool(0), None)
        self.assertEqual(p1.use_tool(2), None)
        p1.add_single_use_tool(2)
        p1.add_single_use_tool(3)
        self.assertEqual(p1.use_tool(3), 2)
        self.assertEqual(p1.use_tool(3), 3)
        self.assertEqual(p1.use_tool(5), None)
        self.assertEqual(p1.use_tool(3), None)

    def test_sufficient_tools(self) -> None:
        goal: int = 1000
        p1 = PlayerTools()

        self.assertFalse(p1.has_sufficient_tools(goal))
        for _ in range(250):
            p1.add_single_use_tool(4)
        self.assertTrue(p1.has_sufficient_tools(goal))
        p1.use_tool(250)
        self.assertFalse(p1.has_sufficient_tools(goal))

    def test_actualize(self) -> None:
        p1 = PlayerTools()

        for _ in range(12):
            p1.add_tool()

        p1.use_tool(0)
        p1.use_tool(1)
        p1.use_tool(2)

        self.assertFalse(p1.has_sufficient_tools(12))
        p1.new_turn()
        self.assertTrue(p1.has_sufficient_tools(12))


if __name__ == '__main__':
    unittest.main()
