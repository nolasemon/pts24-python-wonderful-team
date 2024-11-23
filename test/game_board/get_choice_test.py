import unittest

from stone_age.simple_types import Effect
from stone_age.game_board.get_choice import GetChoice


class GetChoiceTest(unittest.TestCase):
    def test_initialization_empty(self) -> None:
        choice = GetChoice([])
        self.assertEqual(choice.number_of_resources, {})
        self.assertEqual(choice.chosen_resources, {})

    def test_initialization_single(self) -> None:
        choice = GetChoice([Effect.WOOD])
        self.assertEqual(choice.number_of_resources, {Effect.WOOD: 1})
        self.assertEqual(choice.chosen_resources, {})

    def test_initialization_multiple(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY,
                     Effect.WOOD, Effect.CLAY, Effect.CLAY]
        choice = GetChoice(resources)
        self.assertEqual(choice.number_of_resources, {
                         Effect.WOOD: 2, Effect.CLAY: 3})
        self.assertEqual(choice.chosen_resources, {})

    def test_make_choice_valid(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY,
                     Effect.WOOD, Effect.CLAY, Effect.CLAY]
        choice = GetChoice(resources)
        chosen_res = {Effect.WOOD: 1, Effect.CLAY: 2}
        self.assertTrue(choice.make_choice(chosen_res))
        self.assertEqual(choice.chosen_resources, chosen_res)

    def test_make_choice_invalid_resource(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY,
                     Effect.WOOD, Effect.CLAY, Effect.CLAY]
        choice = GetChoice(resources)
        chosen_res = {Effect.STONE: 1}
        self.assertFalse(choice.make_choice(chosen_res))
        self.assertEqual(choice.chosen_resources, {})

    def test_make_choice_invalid_count(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY,
                     Effect.WOOD, Effect.CLAY, Effect.CLAY]
        choice = GetChoice(resources)
        chosen_res = {Effect.WOOD: 3}
        self.assertFalse(choice.make_choice(chosen_res))
        self.assertEqual(choice.chosen_resources, {})

    def test_make_choice_partially_invalid(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY,
                     Effect.WOOD, Effect.CLAY, Effect.CLAY]
        choice = GetChoice(resources)
        chosen_res = {Effect.WOOD: 2, Effect.STONE: 1}
        self.assertFalse(choice.make_choice(chosen_res))
        self.assertEqual(choice.chosen_resources, {})

    def test_state_empty(self) -> None:
        choice = GetChoice([])
        self.assertEqual(choice.state(),
                         "Number of resources to choose from: {}, Chosen resources: {}")

    def test_state_single(self) -> None:
        choice = GetChoice([Effect.WOOD])
        self.assertEqual(choice.state(),
                         "Number of resources to choose from: {<Effect.WOOD: 2>: 1}, "
                         "Chosen resources: {}")

    def test_state_multiple(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY,
                     Effect.WOOD, Effect.CLAY, Effect.CLAY]
        choice = GetChoice(resources)
        expected_state_initial = ("Number of resources to choose from: "
                                  "{<Effect.WOOD: 2>: 2, <Effect.CLAY: 3>: 3}, "
                                  "Chosen resources: {}")
        self.assertEqual(choice.state(), expected_state_initial)

        choice.make_choice({Effect.WOOD: 1, Effect.CLAY: 1})
        expected_state_after_choice = ("Number of resources to choose from: "
                                       "{<Effect.WOOD: 2>: 2, <Effect.CLAY: 3>: 3}, "
                                       "Chosen resources:"
                                       " {<Effect.WOOD: 2>: 1, <Effect.CLAY: 3>: 1}")
        self.assertEqual(choice.state(), expected_state_after_choice)
