import unittest
from typing import List, Iterable
from stone_age.simple_types import ActionResult, Effect, PlayerOrder
from stone_age.game_board.simple_types import Player
from stone_age.game_board.get_something_fixed import GetSomethingFixed
from stone_age.interfaces import InterfacePlayerBoardGameBoard


class TestPlayerBoard(InterfacePlayerBoardGameBoard):
    def __init__(self) -> None:
        self.received_effects: List[Effect] = []

    def give_effect(self, stuff: Iterable[Effect]) -> None:
        self.received_effects.extend(stuff)


class TestGetSomethingFixed(unittest.TestCase):
    def setUp(self) -> None:
        self.player_board = TestPlayerBoard()
        self.player_order = PlayerOrder(order=0, players=2)
        self.player = Player(player_order=self.player_order,
                             player_board=self.player_board)

    def test_effect_property(self) -> None:
        fixed_effect = Effect.FOOD
        action = GetSomethingFixed(effect=fixed_effect)
        self.assertEqual(action.effect, fixed_effect)

    def test_perform_effect_with_choice(self) -> None:
        fixed_effect = Effect.FOOD
        action = GetSomethingFixed(effect=fixed_effect)
        result = action.perform_effect(self.player, choice=Effect.WOOD)
        self.assertEqual(result, ActionResult.FAILURE)
        self.assertEqual(len(self.player_board.received_effects), 0)

    def test_perform_effect_without_choice(self) -> None:
        fixed_effect = Effect.FOOD
        action = GetSomethingFixed(effect=fixed_effect)
        result = action.perform_effect(self.player, choice=None)
        self.assertEqual(result, ActionResult.ACTION_DONE)
        self.assertEqual(len(self.player_board.received_effects), 1)
        self.assertIn(fixed_effect, self.player_board.received_effects)

    def test_state(self) -> None:
        fixed_effect = Effect.FOOD
        action = GetSomethingFixed(effect=fixed_effect)

        self.assertEqual(
            action.state(), f"Effects to be applied: {fixed_effect}")


if __name__ == "__main__":
    unittest.main()
