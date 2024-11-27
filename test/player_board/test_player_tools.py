import unittest
import json

from typing import Any
from stone_age.player_board.player_tools import PlayerTools


class TestPlayerTools(unittest.TestCase):

    def test_tools_adding(self) -> None:
        p1 = PlayerTools()

        p1.add_tool()
        p1.add_tool()

        state_start: Any = json.loads(p1.state())
        self.assertEqual(state_start, {"tools strength": [1, 1, 0],
                                       "used tools": [False, False, False],
                                       "single-use tools": []})
        self.assertFalse(p1.has_sufficient_tools(11))

        for _ in range(4):
            p1.add_tool()

        state_after_adding1: Any = json.loads(p1.state())
        self.assertEqual(state_after_adding1, {"tools strength": [2, 2, 2],
                                               "used tools": [False, False, False],
                                               "single-use tools": []})
        self.assertFalse(p1.has_sufficient_tools(11))

        for _ in range(4):
            p1.add_tool()

        state_after_adding2: Any = json.loads(p1.state())
        self.assertEqual(state_after_adding2, {"tools strength": [4, 3, 3],
                                               "used tools": [False, False, False],
                                               "single-use tools": []})
        self.assertFalse(p1.has_sufficient_tools(11))

        for _ in range(3):
            p1.add_tool()

        state_after_adding3: Any = json.loads(p1.state())
        self.assertEqual(state_after_adding3, {"tools strength": [4, 4, 4],
                                               "used tools": [False, False, False],
                                               "single-use tools": []})
        self.assertTrue(p1.has_sufficient_tools(11))

    def test_figures_taking(self) -> None:
        p1 = PlayerTools()

        for _ in range(10):
            p1.add_tool()

        self.assertTrue(p1.has_sufficient_tools(7))
        p1.use_tool(0)
        self.assertFalse(p1.has_sufficient_tools(7))
        state_after_use1: Any = json.loads(p1.state())
        self.assertEqual(state_after_use1, {"tools strength": [4, 3, 3],
                                            "used tools": [True, False, False],
                                            "single-use tools": []})
        p1.use_tool(1)
        p1.use_tool(2)
        state_after_use2: Any = json.loads(p1.state())
        self.assertEqual(state_after_use2, {"tools strength": [4, 3, 3],
                                            "used tools": [True, True, True],
                                            "single-use tools": []})
        p1.add_tool()
        state_after_add: Any = json.loads(p1.state())
        self.assertEqual(state_after_add, {"tools strength": [4, 4, 3],
                                           "used tools": [True, True, True],
                                           "single-use tools": []})
        self.assertFalse(p1.has_sufficient_tools(4))

    def test_new_turn(self) -> None:
        p1 = PlayerTools()

        for _ in range(10):
            p1.add_tool()

        p1.use_tool(0)
        p1.use_tool(1)

        state_after_use: Any = json.loads(p1.state())
        self.assertEqual(state_after_use, {"tools strength": [4, 3, 3],
                                           "used tools": [True, True, False],
                                           "single-use tools": []})
        p1.new_turn()
        state_new_turn: Any = json.loads(p1.state())
        self.assertEqual(state_new_turn, {"tools strength": [4, 3, 3],
                                          "used tools": [False, False, False],
                                          "single-use tools": []})

    def test_single_use_tool(self) -> None:
        p1 = PlayerTools()

        p1.add_single_use_tool(3)
        state_single_use1: Any = json.loads(p1.state())
        self.assertEqual(state_single_use1, {"tools strength": [0, 0, 0],
                                             "used tools": [False, False, False],
                                             "single-use tools": [3]})
        p1.add_tool()
        p1.add_tool()
        state_add_tools1: Any = json.loads(p1.state())
        self.assertEqual(state_add_tools1, {"tools strength": [1, 1, 0],
                                            "used tools": [False, False, False],
                                            "single-use tools": [3]})
        p1.add_single_use_tool(2)
        state_single_use2: Any = json.loads(p1.state())
        self.assertEqual(state_single_use2, {"tools strength": [1, 1, 0],
                                             "used tools": [False, False, False],
                                             "single-use tools": [3, 2]})
        self.assertTrue(p1.has_sufficient_tools(5))
        p1.use_tool(3)
        state_after_use: Any = json.loads(p1.state())
        self.assertEqual(state_after_use, {"tools strength": [1, 1, 0],
                                           "used tools": [False, False, False],
                                           "single-use tools": [2]})
        self.assertFalse(p1.has_sufficient_tools(5))
        p1.add_tool()
        state_add_tools2: Any = json.loads(p1.state())
        self.assertEqual(state_add_tools2, {"tools strength": [1, 1, 1],
                                            "used tools": [False, False, False],
                                            "single-use tools": [2]})
        p1.new_turn()
        state_new_turn: Any = json.loads(p1.state())
        self.assertEqual(state_new_turn, {"tools strength": [1, 1, 1],
                                          "used tools": [False, False, False],
                                          "single-use tools": [2]})
        p1.add_single_use_tool(1)
        p1.add_single_use_tool(5)
        p1.add_single_use_tool(-1)
        state_single_use3: Any = json.loads(p1.state())
        self.assertEqual(state_single_use3, {"tools strength": [1, 1, 1],
                                             "used tools": [False, False, False],
                                             "single-use tools": [2]})

    def test_add_too_much(self) -> None:
        p1 = PlayerTools()

        for _ in range(100):
            p1.add_tool()

        state_add_too_much: Any = json.loads(p1.state())
        self.assertEqual(state_add_too_much, {"tools strength": [4, 4, 4],
                                              "used tools": [False, False, False],
                                              "single-use tools": []})
        p1.add_single_use_tool(2)
        p1.add_single_use_tool(3)
        p1.add_single_use_tool(4)
        state_add_singles1: Any = json.loads(p1.state())
        self.assertEqual(state_add_singles1, {"tools strength": [4, 4, 4],
                                              "used tools": [False, False, False],
                                              "single-use tools": [2, 3, 4]})
        p1.add_tool()
        p1.add_tool()
        p1.add_single_use_tool(2)
        state_add_singles2: Any = json.loads(p1.state())
        self.assertEqual(state_add_singles2, {"tools strength": [4, 4, 4],
                                              "used tools": [False, False, False],
                                              "single-use tools": [2, 3, 4, 2]})
        p1.use_tool(4)
        p1.use_tool(5)
        state_after_use1: Any = json.loads(p1.state())
        self.assertEqual(state_after_use1, {"tools strength": [4, 4, 4],
                                            "used tools": [False, False, False],
                                            "single-use tools": [2, 4]})
        p1.use_tool(3)
        p1.use_tool(3)
        state_after_use2: Any = json.loads(p1.state())
        self.assertEqual(state_after_use2, {"tools strength": [4, 4, 4],
                                            "used tools": [False, False, False],
                                            "single-use tools": []})

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

    def test_use_two_times(self) -> None:
        p1 = PlayerTools()

        for _ in range(12):
            p1.add_tool()

        p1.use_tool(0)
        p1.use_tool(1)
        p1.use_tool(2)

        state_after_use1: Any = json.loads(p1.state())
        self.assertEqual(state_after_use1, {"tools strength": [4, 4, 4],
                                            "used tools": [True, True, True],
                                            "single-use tools": []})

        self.assertEqual(None, p1.use_tool(1))
        p1.new_turn()
        self.assertEqual(4, p1.use_tool(1))
        p1.add_single_use_tool(2)
        self.assertEqual(2, p1.use_tool(3))
        self.assertEqual(None, p1.use_tool(3))


if __name__ == '__main__':
    unittest.main()
