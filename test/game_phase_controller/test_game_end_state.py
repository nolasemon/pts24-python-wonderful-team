import unittest

from stone_age.game_phase_controller.game_end_state import GameEndState
from stone_age.simple_types import PlayerOrder, HasAction


class TestGameEndState(unittest.TestCase):
    def test_try_automatic_action(self) -> None:
        player = PlayerOrder(1, 1)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         GameEndState().try_to_make_automatic_action(player))
        self.assertRaises(
            AssertionError, GameEndState().do_not_feed_this_turn, player)
