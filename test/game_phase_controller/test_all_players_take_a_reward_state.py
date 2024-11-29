import unittest

from stone_age.game_phase_controller.all_players_take_a_reward_state \
    import AllPlayersTakeARewardState
from stone_age.interfaces import InterfaceTakeReward
from stone_age.simple_types import PlayerOrder, Effect, HasAction, ActionResult


class RewardMock(InterfaceTakeReward):
    _take_response: bool
    _auto_response: HasAction

    def __init__(self, take_reponse: bool = False,
                 auto_response: HasAction = HasAction.NO_ACTION_POSSIBLE):
        self._take_response = take_reponse
        self._auto_response = auto_response

    def take_reward(self, player: PlayerOrder, reward: Effect) -> bool:
        return self._take_response

    def try_make_action(self, player: PlayerOrder) -> HasAction:
        return self._auto_response


class TestAllPlayersRewardState(unittest.TestCase):

    def test_take_reward_method(self) -> None:
        player = PlayerOrder(1, 1)
        reward = Effect.GOLD
        reward_mock = RewardMock()
        all_players_take_fail = AllPlayersTakeARewardState(reward_mock)
        self.assertEqual(ActionResult.FAILURE,
                         all_players_take_fail
                         .make_all_players_take_a_reward_choice(player, reward))
        reward_mock_done = RewardMock(take_reponse=True)
        all_players_take_done = AllPlayersTakeARewardState(reward_mock_done)
        self.assertEqual(ActionResult.ACTION_DONE,
                         all_players_take_done
                         .make_all_players_take_a_reward_choice(player, reward))

    def test_try_to_make_automatic_action_method(self) -> None:
        player = PlayerOrder(1, 1)
        reward_mock_fail = RewardMock()
        automatic_fail = AllPlayersTakeARewardState(reward_mock_fail)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         automatic_fail.try_to_make_automatic_action(player))
        reward_mock_wait = RewardMock(
            auto_response=HasAction.WAITING_FOR_PLAYER_ACTION)
        automatic_wait = AllPlayersTakeARewardState(reward_mock_wait)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         automatic_wait.try_to_make_automatic_action(player))
        reward_mock_done = RewardMock(
            auto_response=HasAction.AUTOMATIC_ACTION_DONE)
        automatic_done = AllPlayersTakeARewardState(reward_mock_done)
        self.assertEqual(HasAction.AUTOMATIC_ACTION_DONE,
                         automatic_done.try_to_make_automatic_action(player))

    def test_wrong_action_tried_this_phase(self) -> None:
        player = PlayerOrder(1, 1)
        mock = RewardMock()
        all_players_take_reward = AllPlayersTakeARewardState(mock)
        self.assertEqual(ActionResult.FAILURE,
                         all_players_take_reward.no_more_tools_this_throw(player))
