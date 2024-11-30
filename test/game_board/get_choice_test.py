import unittest
from unittest.mock import Mock
from typing import Iterable, List
from stone_age.game_board.get_choice import GetChoice
from stone_age.simple_types import Effect, ActionResult
from stone_age.game_board.simple_types import Player
from stone_age.interfaces import InterfacePlayerBoardGameBoard


class TestGetChoice(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_player_board = Mock(spec=InterfacePlayerBoardGameBoard)
        self.mock_player = Mock(spec=Player)
        self.mock_player.player_board = self.mock_player_board
        self.get_choice = GetChoice(2)

    def test_perform_effect_valid_choice(self) -> None:
        choice: Iterable[Effect] = [Effect.WOOD, Effect.CLAY]
        result = self.get_choice.perform_effect(self.mock_player, choice)
        self.assertEqual(result, ActionResult.ACTION_DONE)
        self.mock_player_board.give_effect.assert_called_once_with(
            list(choice))

    def test_perform_effect_invalid_choice_not_iterable(self) -> None:
        choice: Effect = Effect.WOOD
        result = self.get_choice.perform_effect(self.mock_player, [choice])
        self.assertEqual(result, ActionResult.FAILURE)
        self.mock_player_board.give_effect.assert_not_called()

    def test_perform_effect_invalid_choice_too_many_resources(self) -> None:
        choice: Iterable[Effect] = [Effect.WOOD, Effect.CLAY, Effect.STONE]
        result = self.get_choice.perform_effect(self.mock_player, choice)
        self.assertEqual(result, ActionResult.FAILURE)
        self.mock_player_board.give_effect.assert_not_called()

    def test_perform_effect_invalid_choice_not_a_resource(self) -> None:
        choice: Iterable[Effect] = [Effect.WOOD, Effect.FOOD]
        result = self.get_choice.perform_effect(self.mock_player, choice)
        self.assertEqual(result, ActionResult.FAILURE)
        self.mock_player_board.give_effect.assert_not_called()

    def test_perform_effect_invalid_choice_empty(self) -> None:
        choice: List[Effect] = []
        result = self.get_choice.perform_effect(self.mock_player, choice)
        self.assertEqual(result, ActionResult.FAILURE)
        self.mock_player_board.give_effect.assert_not_called()
