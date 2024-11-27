import unittest
from typing import Mapping

from stone_age.game_phase_controller.new_round_state import NewRoundState
from stone_age.interfaces import InterfaceFigureLocation, InterfaceNewTurn
from stone_age.simple_types import PlayerOrder, HasAction, Location, ActionResult


class LocationMock(InterfaceFigureLocation):
    _new_turn_response: bool

    def __init__(self, new_turn_response: bool):
        self._new_turn_response = new_turn_response

    def new_turn(self) -> bool:
        return self._new_turn_response


class NewTurnFake(InterfaceNewTurn):
    def new_turn(self) -> None:
        pass


class TestNewRoundState(unittest.TestCase):
    def test_no_game_end(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(False),
            Location.CIVILISATION_CARD1: LocationMock(False),
            Location.FIELD: LocationMock(False)
        }
        new_round_state = NewRoundState(
            places, {PlayerOrder(1, 4): NewTurnFake()})
        player = PlayerOrder(1, 1)
        self.assertEqual(HasAction.AUTOMATIC_ACTION_DONE,
                         new_round_state.try_to_make_automatic_action(player))

    def test_game_end(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(False),
            Location.CIVILISATION_CARD1: LocationMock(True),
            Location.FIELD: LocationMock(False)
        }
        new_round_state = NewRoundState(
            places, {PlayerOrder(1, 4): NewTurnFake()})
        player = PlayerOrder(1, 1)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         new_round_state.try_to_make_automatic_action(player))

    def test_failure_method(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(False),
            Location.CIVILISATION_CARD1: LocationMock(True),
        }
        new_round_state = NewRoundState(
            places, {PlayerOrder(1, 4): NewTurnFake()})
        player = PlayerOrder(1, 1)
        self.assertEqual(ActionResult.FAILURE,
                         new_round_state.do_not_feed_this_turn(player))
