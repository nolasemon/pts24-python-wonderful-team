import unittest
from unittest.mock import Mock

from stone_age.game_board.get_something_throw import GetSomethingThrow
from stone_age.game_board.interfaces import InterfaceCurrentThrow
from stone_age.simple_types import Effect, ActionResult
from stone_age.game_board.simple_types import Player


class TestGetSomethingThrow(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_current_throw = Mock(spec=InterfaceCurrentThrow)
        self.mock_player = Mock(spec=Player)

    def test_perform_effect_wood(self) -> None:
        get_something_throw = GetSomethingThrow(
            self.mock_current_throw, Effect.WOOD)
        result = get_something_throw.perform_effect(
            self.mock_player, [Effect.WOOD])
        self.assertEqual(result, ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE)
        self.mock_current_throw.initiate.assert_called_once_with(
            self.mock_player, Effect.WOOD, 2)

    def test_perform_effect_clay(self) -> None:
        get_something_throw = GetSomethingThrow(
            self.mock_current_throw, Effect.CLAY)
        result = get_something_throw.perform_effect(
            self.mock_player, [Effect.CLAY])
        self.assertEqual(result, ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE)
        self.mock_current_throw.initiate.assert_called_once_with(
            self.mock_player, Effect.CLAY, 2)

    def test_perform_effect_empty_choice(self) -> None:
        get_something_throw = GetSomethingThrow(
            self.mock_current_throw, Effect.WOOD)
        result = get_something_throw.perform_effect(self.mock_player, [])
        self.assertEqual(result, ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE)
        self.mock_current_throw.initiate.assert_called_once_with(
            self.mock_player, Effect.WOOD, 2)

    def test_perform_effect_different_choice(self) -> None:
        get_something_throw = GetSomethingThrow(
            self.mock_current_throw, Effect.WOOD)
        result = get_something_throw.perform_effect(
            self.mock_player, [Effect.CLAY])
        self.assertEqual(result, ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE)
        self.mock_current_throw.initiate.assert_called_once_with(
            self.mock_player, Effect.WOOD, 2)
