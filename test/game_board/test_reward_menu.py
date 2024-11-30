import unittest
from typing import List, Dict, Iterable, cast
from stone_age.simple_types import Effect, HasAction, PlayerOrder
from stone_age.game_board.simple_types import Player
from stone_age.game_board.reward_menu import RewardMenu
from stone_age.interfaces import InterfacePlayerBoardGameBoard


class TestPlayerBoard(InterfacePlayerBoardGameBoard):
    def __init__(self) -> None:
        self.received_effects: List[Effect] = []

    def give_effect(self, stuff: Iterable[Effect]) -> None:
        self.received_effects.extend(stuff)


class TestRewardMenu(unittest.TestCase):
    def setUp(self) -> None:
        self.players: Dict[PlayerOrder, Player] = {
            PlayerOrder(order=0, players=2): Player(
                player_order=PlayerOrder(order=0, players=2),
                player_board=TestPlayerBoard()
            ),
            PlayerOrder(order=1, players=2): Player(
                player_order=PlayerOrder(order=1, players=2),
                player_board=TestPlayerBoard()
            ),
        }

        self.reward_menu = RewardMenu(players=self.players)

    def test_initiate(self) -> None:
        rewards: List[Effect] = [Effect.WOOD, Effect.FOOD]
        self.reward_menu.initiate(rewards)
        self.assertEqual(self.reward_menu.menu, rewards)

    def test_take_reward_success(self) -> None:
        rewards: List[Effect] = [Effect.WOOD, Effect.FOOD]
        self.reward_menu.initiate(rewards)

        player_order = PlayerOrder(order=0, players=2)
        player_board = cast(TestPlayerBoard, self.players[player_order].player_board)

        result = self.reward_menu.take_reward(player_order, Effect.WOOD)
        self.assertTrue(result)
        self.assertEqual(len(player_board.received_effects), 1)
        self.assertIn(Effect.WOOD, player_board.received_effects)
        self.assertNotIn(Effect.WOOD, self.reward_menu.menu)

    def test_take_reward_failure(self) -> None:
        rewards: List[Effect] = [Effect.WOOD]
        self.reward_menu.initiate(rewards)

        player_order = PlayerOrder(order=0, players=2)
        player_board = cast(TestPlayerBoard, self.players[player_order].player_board)

        result = self.reward_menu.take_reward(player_order, Effect.FOOD)
        self.assertFalse(result)
        self.assertEqual(len(player_board.received_effects), 0)
        self.assertNotIn(Effect.FOOD, self.reward_menu.menu)

    def test_try_make_action_automatic(self) -> None:
        rewards: List[Effect] = [Effect.FOOD]
        self.reward_menu.initiate(rewards)

        player_order = PlayerOrder(order=0, players=2)
        player_board = cast(TestPlayerBoard, self.players[player_order].player_board)

        result = self.reward_menu.try_make_action(player_order)
        self.assertEqual(result, HasAction.AUTOMATIC_ACTION_DONE)
        self.assertEqual(len(player_board.received_effects), 1)
        self.assertIn(Effect.FOOD, player_board.received_effects)
        self.assertEqual(len(self.reward_menu.menu), 0)

    def test_try_make_action_waiting(self) -> None:
        rewards: List[Effect] = [Effect.WOOD, Effect.FOOD]
        self.reward_menu.initiate(rewards)

        player_order = PlayerOrder(order=0, players=2)
        result = self.reward_menu.try_make_action(player_order)
        self.assertEqual(result, HasAction.WAITING_FOR_PLAYER_ACTION)

    def test_try_make_action_no_action(self) -> None:
        rewards: List[Effect] = []
        self.reward_menu.initiate(rewards)

        player_order = PlayerOrder(order=0, players=2)
        result = self.reward_menu.try_make_action(player_order)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_state(self) -> None:
        rewards: List[Effect] = [Effect.WOOD, Effect.FOOD]
        self.reward_menu.initiate(rewards)

        expected_state = '{"menu content": ["WOOD", "FOOD"]}'
        self.assertEqual(self.reward_menu.state(), expected_state)


if __name__ == "__main__":
    unittest.main()
