import unittest
from typing import Iterable

from stone_age.game_phase_controller.feed_tribe_state import FeedTribeState
from stone_age.interfaces import InterfaceFeedTribe
from stone_age.simple_types import PlayerOrder, ActionResult, HasAction, Effect

class FeedMock(InterfaceFeedTribe):
    _enough_response: bool
    _feed_response: bool
    _do_not_response: bool
    _is_fed_response: bool

    def __init__(self, enough_response: bool = False, feed_response: bool = False,
                 do_not_response:bool = False, is_fed_response: bool = False):
        self._enough_response = enough_response
        self._feed_response = feed_response
        self._do_not_response = do_not_response
        self._is_fed_response = is_fed_response

    def feed_tribe_if_enough_food(self) -> bool:
        return self._enough_response

    def feed_tribe(self, resources: Iterable[Effect]) -> bool:
        return self._feed_response

    def do_not_feed_this_turn(self) -> bool:
        return self._do_not_response

    def is_tribe_fed(self) -> bool:
        return self._is_fed_response


class TestFeedTribeState(unittest.TestCase):

    def test_feed_tribe_method(self) -> None:
        player = PlayerOrder(1,1)
        resources: Iterable[Effect] = []
        mock_failure = FeedMock()
        feed_tribe_state = FeedTribeState(mock_failure)
        self.assertEqual(ActionResult.FAILURE,
                         feed_tribe_state.feed_tribe(player, resources))
        mock_done = FeedMock(feed_response=True)
        feed_tribe_state = FeedTribeState(mock_done)
        self.assertEqual(ActionResult.ACTION_DONE,
                         feed_tribe_state.feed_tribe(player, resources))

    def test_do_not_feed_this_turn_method(self) -> None:
        player = PlayerOrder(1,1)
        mock_failure = FeedMock()
        feed_tribe_state = FeedTribeState(mock_failure)
        self.assertEqual(ActionResult.FAILURE,
                         feed_tribe_state.do_not_feed_this_turn(player))
        mock_done = FeedMock(do_not_response=True)
        feed_tribe_state = FeedTribeState(mock_done)
        self.assertEqual(ActionResult.ACTION_DONE,
                         feed_tribe_state.do_not_feed_this_turn(player))

    def test_try_to_make_automatic_action_method(self) -> None:
        player = PlayerOrder(1,1)
        mock_wait = FeedMock()
        feed_tribe_state = FeedTribeState(mock_wait)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         feed_tribe_state.try_to_make_automatic_action(player))
        mock_done = FeedMock(enough_response=True)
        feed_tribe_state = FeedTribeState(mock_done)
        self.assertEqual(HasAction.AUTOMATIC_ACTION_DONE,
                         feed_tribe_state.try_to_make_automatic_action(player))

    def test_automatic_action_fed_tribe(self) -> None:
        player = PlayerOrder(1,1)
        mock_is_fed = FeedMock(is_fed_response=True)
        feed_tribe_state = FeedTribeState(mock_is_fed)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         feed_tribe_state.try_to_make_automatic_action(player))
        mock_enough_food_but_fed = FeedMock(enough_response=True,
                                            is_fed_response=True)
        feed_tribe_state = FeedTribeState(mock_enough_food_but_fed)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         feed_tribe_state.try_to_make_automatic_action(player))

    def test_wrong_action_tried_this_phase(self) -> None:
        player = PlayerOrder(1,1)
        idx: int = 1
        mock = FeedMock()
        feed_tribe_state = FeedTribeState(mock)
        self.assertEqual(ActionResult.FAILURE,
                         feed_tribe_state.use_tools(player, idx))
