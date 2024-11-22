import unittest
from typing import Iterable, Mapping

from stone_age.game_phase_controller.make_action_state import MakeActionState
from stone_age.interfaces import InterfaceFigureLocation
from stone_age.simple_types import PlayerOrder, HasAction, Effect, ActionResult, Location


class LocationMock(InterfaceFigureLocation):
    _make_response: ActionResult
    _skip_response: bool
    _try_response: HasAction

    def __init__(self, make_response: ActionResult = ActionResult.FAILURE,
                 skip_response: bool = False,
                 try_response: HasAction = HasAction.NO_ACTION_POSSIBLE):
        self._make_response = make_response
        self._skip_response = skip_response
        self._try_response = try_response

    def place_figures(self, player: PlayerOrder, figure_count: int) -> bool:
        assert False

    def try_to_place_figures(self, player: PlayerOrder, count: int) -> HasAction:
        assert False

    def make_action(self, player: PlayerOrder, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        return self._make_response

    def skip_action(self, player: PlayerOrder) -> bool:
        return self._skip_response

    def try_to_make_action(self, player: PlayerOrder) -> HasAction:
        return self._try_response

    def new_turn(self) -> bool:
        assert False


class TestMakeActionState(unittest.TestCase):
    def test_make_action_method(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(ActionResult.ACTION_DONE),
            Location.FIELD: LocationMock(ActionResult.FAILURE),
            Location.QUARY: LocationMock(ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE),
        }
        player = PlayerOrder(1, 1)
        place_figures_state = MakeActionState(places)
        input_resources: Iterable[Effect] = []
        output_resources: Iterable[Effect] = []
        self.assertEqual(ActionResult.ACTION_DONE,
                         place_figures_state.make_action(player, Location.HUT,
                                                         input_resources, output_resources))
        self.assertEqual(ActionResult.FAILURE,
                         place_figures_state.make_action(player, Location.FIELD,
                                                         input_resources, output_resources))
        self.assertEqual(ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE,
                         place_figures_state.make_action(player, Location.QUARY,
                                                         input_resources, output_resources))

    def test_skip_action_method(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(skip_response=True),
            Location.FIELD: LocationMock(skip_response=False),
        }
        player = PlayerOrder(1, 1)
        make_action_state = MakeActionState(places)
        self.assertEqual(ActionResult.ACTION_DONE,
                         make_action_state.skip_action(player, Location.HUT))
        self.assertEqual(ActionResult.FAILURE,
                         make_action_state.skip_action(player, Location.FIELD))

    def test_try_automatic_action_all_locations_impossible(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.FIELD: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.QUARY: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
        }
        player = PlayerOrder(1, 1)
        make_action_state = MakeActionState(places)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         make_action_state.try_to_make_automatic_action(player))

    def test_try_automatic_action_one_waiting_location(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.FIELD: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION),
            Location.QUARY: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
        }
        player = PlayerOrder(1, 1)
        make_action_state = MakeActionState(places)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         make_action_state.try_to_make_automatic_action(player))

    def test_try_automatic_action_automatic_done(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.FIELD: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.QUARY: LocationMock(try_response=HasAction.AUTOMATIC_ACTION_DONE),
        }
        player = PlayerOrder(1, 1)
        make_action_state = MakeActionState(places)
        self.assertEqual(HasAction.AUTOMATIC_ACTION_DONE,
                         make_action_state.try_to_make_automatic_action(player))

    def test_try_automatic_action_mix(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.FIELD: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.BUILDING_TILE1: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION),
            Location.QUARY: LocationMock(try_response=HasAction.AUTOMATIC_ACTION_DONE),
            Location.BUILDING_TILE2: LocationMock(try_response=HasAction.WAITING_FOR_PLAYER_ACTION),
            Location.FOREST: LocationMock(try_response=HasAction.AUTOMATIC_ACTION_DONE),
            Location.HUNTING_GROUNDS: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
        }
        player = PlayerOrder(1, 1)
        make_action_state = MakeActionState(places)
        self.assertEqual(HasAction.AUTOMATIC_ACTION_DONE,
                         make_action_state.try_to_make_automatic_action(player))

    def test_wrong_method_called(self) -> None:
        places: Mapping[Location, LocationMock] = {
            Location.HUT: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.FIELD: LocationMock(try_response=HasAction.NO_ACTION_POSSIBLE),
            Location.QUARY: LocationMock(try_response=HasAction.AUTOMATIC_ACTION_DONE),
        }
        player = PlayerOrder(1, 1)
        make_action_state = MakeActionState(places)
        self.assertEqual(ActionResult.FAILURE,
                         make_action_state.no_more_tools_this_throw(player))
