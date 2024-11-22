import unittest

from stone_age.simple_types import Effect, HasAction, PlayerOrder
from stone_age.game_board.all_players_take_reward import AllPlayersTakeReward


class AllPlayersTakeRewardTest(unittest.TestCase):
    def test_initiate(self) -> None:
        reward = AllPlayersTakeReward()
        menu = [Effect.WOOD, Effect.CLAY, Effect.STONE]
        players = [PlayerOrder(0, 3), PlayerOrder(1, 3), PlayerOrder(2, 3)]
        reward.initiate(menu, players)
        self.assertEqual(reward.menu, menu)
        self.assertEqual(reward.players, players)
        self.assertEqual(reward.current_player_index, 0)

    def test_try_make_action_no_menu(self) -> None:
        reward = AllPlayersTakeReward()
        players = [PlayerOrder(0, 1)]
        reward.initiate([], players)
        self.assertEqual(reward.try_make_action(
            players[0]), HasAction.NO_ACTION_POSSIBLE)

    def test_try_make_action_wrong_player(self) -> None:
        reward = AllPlayersTakeReward()
        menu = [Effect.WOOD, Effect.CLAY]
        players = [PlayerOrder(0, 2), PlayerOrder(1, 2)]
        reward.initiate(menu, players)
        self.assertEqual(reward.try_make_action(
            players[1]), HasAction.NO_ACTION_POSSIBLE)

    def test_try_make_action_correct_player(self) -> None:
        reward = AllPlayersTakeReward()
        menu = [Effect.WOOD, Effect.CLAY]
        players = [PlayerOrder(0, 2), PlayerOrder(1, 2)]
        reward.initiate(menu, players)
        self.assertEqual(reward.try_make_action(
            players[0]), HasAction.WAITING_FOR_PLAYER_ACTION)

    def test_take_reward_empty_menu(self) -> None:
        reward = AllPlayersTakeReward()
        players = [PlayerOrder(0, 1)]
        reward.initiate([], players)
        self.assertFalse(reward.take_reward(players[0], Effect.WOOD))

    def test_take_reward_wrong_player(self) -> None:
        reward = AllPlayersTakeReward()
        menu = [Effect.WOOD, Effect.CLAY]
        players = [PlayerOrder(0, 2), PlayerOrder(1, 2)]
        reward.initiate(menu, players)
        self.assertFalse(reward.take_reward(players[1], Effect.WOOD))

    def test_take_reward_invalid_reward(self) -> None:
        reward = AllPlayersTakeReward()
        menu = [Effect.WOOD, Effect.CLAY]
        players = [PlayerOrder(0, 2), PlayerOrder(1, 2)]
        reward.initiate(menu, players)
        self.assertFalse(reward.take_reward(players[0], Effect.STONE))

    def test_take_reward_correct(self) -> None:
        reward = AllPlayersTakeReward()
        menu = [Effect.WOOD, Effect.CLAY]
        players = [PlayerOrder(0, 2), PlayerOrder(1, 2)]
        reward.initiate(menu, players)
        self.assertTrue(reward.take_reward(players[0], Effect.WOOD))
        self.assertEqual(reward.menu, [Effect.CLAY])
        self.assertEqual(reward.current_player_index, 1)

    def test_take_all_rewards(self) -> None:
        reward = AllPlayersTakeReward()
        menu = [Effect.WOOD, Effect.CLAY, Effect.STONE]
        players = [PlayerOrder(0, 3), PlayerOrder(1, 3), PlayerOrder(2, 3)]
        reward.initiate(menu, players)
        self.assertTrue(reward.take_reward(players[0], Effect.WOOD))
        self.assertTrue(reward.take_reward(players[1], Effect.CLAY))
        self.assertTrue(reward.take_reward(players[2], Effect.STONE))
        self.assertEqual(reward.menu, [])
        self.assertEqual(reward.current_player_index, 0)

    def test_state(self) -> None:
        reward = AllPlayersTakeReward()
        menu = [Effect.WOOD, Effect.CLAY]
        players = [PlayerOrder(0, 2), PlayerOrder(1, 2)]
        reward.initiate(menu, players)
        expected_state_start = "Menu: [<Effect.WOOD: 2>, <Effect.CLAY: 3>], Players: ["
        expected_state_end = "], Current Player Index: 0"
        actual_state = reward.state()
        self.assertTrue(actual_state.startswith(expected_state_start))
        self.assertTrue(actual_state.endswith(expected_state_end))
