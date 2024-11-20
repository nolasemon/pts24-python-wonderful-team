import unittest
from typing import Iterable, Mapping

from stone_age.game_phase_controller.place_figures_state import PlaceFiguresState
from stone_age.interfaces import InterfaceFigureLocation
from stone_age.simple_types import PlayerOrder, HasAction, Effect, ActionResult, Location


class LocationMock(InterfaceFigureLocation):
    _place_response: bool
    _try_response: HasAction

    def __init__(self, place_response: bool = False,
                 try_response: HasAction = HasAction.NO_ACTION_POSSIBLE):
        self._place_response = place_response
        self._try_response = try_response

    def place_figures(self, player: PlayerOrder, figure_count: int) -> bool:
        return self._place_response

    def try_to_place_figures(self, player: PlayerOrder, count: int) -> HasAction:
        return self._try_response

    def make_action(self, player: PlayerOrder, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert False

    def skip_action(self, player: PlayerOrder) -> bool:
        assert False

    def try_to_make_action(self, player: PlayerOrder) -> HasAction:
        assert False

    def new_turn(self) -> bool:
        assert False


class TestPlaceFiguresState(unittest.TestCase):
    def test_place_figures_method(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(True),
            Location.FIELD: LocationMock(False),
        }
        player = PlayerOrder(1, 1)
        place_figures_state = PlaceFiguresState(places)
        self.assertEqual(ActionResult.ACTION_DONE,
                         place_figures_state.place_figures(player, Location.HUT, 1))
        self.assertEqual(ActionResult.FAILURE,
                         place_figures_state.place_figures(player, Location.FIELD, 1))

    def test_try_automatic_action_one_location(self) -> None:
        places = {
            Location.HUT: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION),
        }
        player = PlayerOrder(1, 1)
        place_figures_state = PlaceFiguresState(places)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         place_figures_state.try_to_make_automatic_action(player))

    def test_try_automatic_action_no_good_location(self) -> None:
        places = {
            Location.HUT: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.QUARY: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.CIVILISATION_CARD1: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.BUILDING_TILE1: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE)
        }
        player = PlayerOrder(1, 1)
        place_figures_state = PlaceFiguresState(places)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         place_figures_state.try_to_make_automatic_action(player))

    def test_try_automatic_action_one_good_location(self) -> None:
        places = {
            Location.HUT: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.QUARY: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION),
            Location.CIVILISATION_CARD1: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.BUILDING_TILE1: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE)
        }
        player = PlayerOrder(1, 1)
        place_figures_state = PlaceFiguresState(places)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         place_figures_state.try_to_make_automatic_action(player))

    def test_try_automatic_action_all_good_locations(self) -> None:
        places = {
            Location.HUT: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION),
            Location.QUARY: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION),
            Location.CIVILISATION_CARD1: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION),
            Location.BUILDING_TILE1: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION)
        }
        player = PlayerOrder(1, 1)
        place_figures_state = PlaceFiguresState(places)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         place_figures_state.try_to_make_automatic_action(player))