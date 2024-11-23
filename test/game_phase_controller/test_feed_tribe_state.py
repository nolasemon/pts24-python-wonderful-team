import unittest
from typing import Iterable, Mapping

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
        dict_player_interface1: Mapping[PlayerOrder, FeedMock] = {player: mock_failure}
        feed_tribe_state = FeedTribeState(dict_player_interface1)
        self.assertEqual(ActionResult.FAILURE,
                         feed_tribe_state.feed_tribe(player, resources))
        mock_done = FeedMock(feed_response=True)
        dict_player_interface2: Mapping[PlayerOrder, FeedMock] = {player: mock_done}
        feed_tribe_state = FeedTribeState(dict_player_interface2)
        self.assertEqual(ActionResult.ACTION_DONE,
                         feed_tribe_state.feed_tribe(player, resources))

    def test_do_not_feed_this_turn_method(self) -> None:
        player = PlayerOrder(1,1)
        mock_failure = FeedMock()
        dict_player_interface1: Mapping[PlayerOrder, FeedMock] = {player: mock_failure}
        feed_tribe_state = FeedTribeState(dict_player_interface1)
        self.assertEqual(ActionResult.FAILURE,
                         feed_tribe_state.do_not_feed_this_turn(player))
        mock_done = FeedMock(do_not_response=True)
        dict_player_interface2: Mapping[PlayerOrder, FeedMock] = {player: mock_done}
        feed_tribe_state = FeedTribeState(dict_player_interface2)
        self.assertEqual(ActionResult.ACTION_DONE,
                         feed_tribe_state.do_not_feed_this_turn(player))

    def test_try_to_make_automatic_action_method(self) -> None:
        player = PlayerOrder(1,1)
        mock_wait = FeedMock()
        dict_player_interface1: Mapping[PlayerOrder, FeedMock] = {player: mock_wait}
        feed_tribe_state = FeedTribeState(dict_player_interface1)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         feed_tribe_state.try_to_make_automatic_action(player))
        mock_done = FeedMock(enough_response=True)
        dict_player_interface2: Mapping[PlayerOrder, FeedMock] = {player: mock_done}
        feed_tribe_state = FeedTribeState(dict_player_interface2)
        self.assertEqual(HasAction.AUTOMATIC_ACTION_DONE,
                         feed_tribe_state.try_to_make_automatic_action(player))

    def test_automatic_action_fed_tribe(self) -> None:
        player = PlayerOrder(1,1)
        mock_is_fed = FeedMock(is_fed_response=True)
        dict_player_interface1: Mapping[PlayerOrder, FeedMock] = {player: mock_is_fed}
        feed_tribe_state = FeedTribeState(dict_player_interface1)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         feed_tribe_state.try_to_make_automatic_action(player))
        mock_enough_food_but_fed = FeedMock(enough_response=True,
                                            is_fed_response=True)
        dict_player_interface2: Mapping[PlayerOrder, FeedMock] = {player: mock_enough_food_but_fed}
        feed_tribe_state = FeedTribeState(dict_player_interface2)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         feed_tribe_state.try_to_make_automatic_action(player))

    def test_wrong_action_tried_this_phase(self) -> None:
        player = PlayerOrder(1,1)
        idx: int = 1
        mock = FeedMock()
        dict_player_interface: Mapping[PlayerOrder, FeedMock] = {player: mock}
        feed_tribe_state = FeedTribeState(dict_player_interface)
        self.assertEqual(ActionResult.FAILURE,
                         feed_tribe_state.use_tools(player, idx))
