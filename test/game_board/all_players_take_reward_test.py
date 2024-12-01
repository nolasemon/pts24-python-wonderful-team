import unittest
from unittest.mock import Mock

from stone_age.game_board.all_players_take_reward import AllPlayersTakeReward
from stone_age.game_board.throw import Throw
from stone_age.interfaces import InterfaceTakeReward
from stone_age.simple_types import PlayerOrder, Effect, ActionResult
from stone_age.game_board.simple_types import Player


class TestAllPlayersTakeReward(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_reward_menu = Mock(spec=InterfaceTakeReward)
        self.mock_throw = Mock(spec=Throw)
        self.mock_player = Mock(spec=Player)

    def test_perform_effect_valid_throws(self) -> None:
        self.mock_throw.throw.return_value = [1, 2, 3, 4, 5, 6]
        self.mock_player.player_order = PlayerOrder(0, 6)
        action = AllPlayersTakeReward(self.mock_reward_menu, self.mock_throw)
        result = action.perform_effect(self.mock_player, [])
        self.assertEqual(
            result, ActionResult.ACTION_DONE_ALL_PLAYERS_TAKE_A_REWARD)
        self.mock_throw.throw.assert_called_with(1)
        self.mock_reward_menu.initiate.assert_called_once_with([
            Effect.WOOD, Effect.CLAY, Effect.STONE, Effect.GOLD, Effect.TOOL, Effect.FIELD
        ])

    def test_perform_effect_invalid_throw_result_low(self) -> None:
        self.mock_throw.throw.return_value = [0, 1, 2]
        self.mock_player.player_order = PlayerOrder(0, 3)
        action = AllPlayersTakeReward(self.mock_reward_menu, self.mock_throw)
        with self.assertRaises(ValueError):
            action.perform_effect(self.mock_player, [])

    def test_perform_effect_invalid_throw_result_high(self) -> None:
        self.mock_throw.throw.return_value = [1, 2, 7]
        self.mock_player.player_order = PlayerOrder(0, 3)
        action = AllPlayersTakeReward(self.mock_reward_menu, self.mock_throw)
        with self.assertRaises(ValueError):
            action.perform_effect(self.mock_player, [])
