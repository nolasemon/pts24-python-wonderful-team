# pylint: disable=too-many-instance-attributes
import unittest

from typing import List, Mapping
import json

from test.game_phase_controller.test_integration.interface_mocks import \
    LocationMock, NewTurnMock, FeedTribeMock, ToolUseMock, RewardMock
from stone_age.game_phase_controller.factories import game_phase_controller_factory
from stone_age.interfaces import InterfaceGamePhaseController
from stone_age.simple_types import Location, PlayerOrder, ActionResult, HasAction


class GamePhaseControllerIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.n: int
        self.players: List[PlayerOrder]
        self.locations: Mapping[Location, LocationMock]
        self.tool_use: ToolUseMock
        self.reward: RewardMock
        self.new_turns: Mapping[PlayerOrder, NewTurnMock]
        self.feed_tribes: Mapping[PlayerOrder, FeedTribeMock]
        self.gpc: InterfaceGamePhaseController

    def mock_setup(self, player_number: int, locations: List[Location]) -> None:
        self.n = player_number
        self.players = []
        for i in range(self.n):
            self.players.append(PlayerOrder(i, self.n))
        self.locations = {
            location: LocationMock() for location in locations
        }
        self.tool_use = ToolUseMock()
        self.reward = RewardMock()
        self.new_turns = {player: NewTurnMock() for player in self.players}
        self.feed_tribes = {player: FeedTribeMock() for player in self.players}
        self.gpc = game_phase_controller_factory(
            self.locations,
            self.tool_use,
            self.reward,
            self.new_turns,
            self.feed_tribes,
            self.players[0]
        )

    def test_minimal_game(self) -> None:
        self.mock_setup(2, [Location.TOOL_MAKER])
        self.locations[Location.TOOL_MAKER].place_responses = [True] * self.n
        self.locations[Location.TOOL_MAKER].try_place_responses = [
            HasAction.NO_ACTION_POSSIBLE] * self.n
        self.locations[Location.TOOL_MAKER].try_make_responses = [
            HasAction.NO_ACTION_POSSIBLE] * self.n
        for player in self.players:
            self.feed_tribes[player].is_fed_responses = [True] * self.n
        self.locations[Location.TOOL_MAKER].new_turn_responses = [
            True] * self.n

        # we start in PlaceFigures phase
        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        # we called place_figures, now controller tries to make automatic action for all players
        # try_to_place_figures is negative for all players, so we move to MakeAction phase
        # try_to_make_action is negative for all players, so we move to FeedTribe phase
        # all tribes are fed (on virtually only), so we move to NewTurn phase
        # output True from location on new_turn signifies GameEnd phase
        state = json.loads(self.gpc.state())
        self.assertEqual(state["game phase"], "GamePhase.GAME_END")

    def test_waiting_for_placing(self) -> None:
        self.mock_setup(2, [Location.TOOL_MAKER])
        self.locations[Location.TOOL_MAKER].place_responses = [True]
        self.locations[Location.TOOL_MAKER].try_place_responses = [
            HasAction.WAITING_FOR_PLAYER_ACTION]

        # we start in PlaceFigures phase
        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        # now try_to_place_figures returned waiting for player action, so we are still in this phase
        state = json.loads(self.gpc.state())
        self.assertEqual(state["game phase"], "GamePhase.PLACE_FIGURES")

    def test_consequent_placing(self) -> None:
        self.mock_setup(2, [Location.TOOL_MAKER])
        self.locations[Location.TOOL_MAKER].place_responses = [True] * 2
        self.locations[Location.TOOL_MAKER].try_place_responses = [
            HasAction.WAITING_FOR_PLAYER_ACTION] * 2

        # we start in PlaceFigures phase
        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        # now try_to_place_figures returned waiting for player action, so we are still in this phase
        # player 0 can not place figure second time before player 1 places his figure
        self.assertFalse(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        self.assertTrue(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))

    def test_multiple_placing(self) -> None:
        self.mock_setup(3, [Location.TOOL_MAKER])
        self.locations[Location.TOOL_MAKER].place_responses = [True] * 6
        self.locations[Location.TOOL_MAKER].try_place_responses = [
            HasAction.WAITING_FOR_PLAYER_ACTION] * 6

        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        self.assertTrue(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))
        self.assertTrue(self.gpc.place_figures(self.players[2], Location.TOOL_MAKER, 1))
        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        self.assertFalse(self.gpc.place_figures(self.players[2], Location.TOOL_MAKER, 1))
        self.assertTrue(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))
        self.assertFalse(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        self.assertTrue(self.gpc.place_figures(self.players[2], Location.TOOL_MAKER, 1))

    def test_multiple_placing2(self) -> None:
        self.mock_setup(3, [Location.TOOL_MAKER])
        self.locations[Location.TOOL_MAKER].place_responses = [True] * 6
        self.locations[Location.TOOL_MAKER].try_place_responses = [  # player 0 ok
            HasAction.NO_ACTION_POSSIBLE,  # player 1 impossible
            HasAction.WAITING_FOR_PLAYER_ACTION,  # waiting for player 2
            HasAction.NO_ACTION_POSSIBLE,  # player 0 impossible
            HasAction.WAITING_FOR_PLAYER_ACTION,  # waiting for player 1
            HasAction.WAITING_FOR_PLAYER_ACTION,  # waiting for player 2
        ]

        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        # now we skip player 1
        self.assertFalse(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))
        self.assertTrue(self.gpc.place_figures(self.players[2], Location.TOOL_MAKER, 1))
        # now we skip player 0
        self.assertTrue(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))
        # waiting for player 2, all other return False
        self.assertFalse(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        self.assertFalse(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))

    def test_multiple_placing3(self) -> None:
        self.mock_setup(3, [Location.TOOL_MAKER])
        self.locations[Location.TOOL_MAKER].place_responses = [True, False] * 3
        self.locations[Location.TOOL_MAKER].try_place_responses = [
            HasAction.WAITING_FOR_PLAYER_ACTION] * 6

        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        self.assertFalse(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))
        # player 1 unsuccessful, he must try again
        self.assertTrue(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))
        self.assertFalse(self.gpc.place_figures(self.players[2], Location.TOOL_MAKER, 1))
        # player 2 unsuccessful, he must try again
        self.assertTrue(self.gpc.place_figures(self.players[2], Location.TOOL_MAKER, 1))
        self.assertFalse(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))

    def test_making_simple(self) -> None:
        self.mock_setup(2, [Location.TOOL_MAKER])
        self.locations[Location.TOOL_MAKER].place_responses = [True] * 2
        self.locations[Location.TOOL_MAKER].try_place_responses = \
            [HasAction.WAITING_FOR_PLAYER_ACTION] + [HasAction.NO_ACTION_POSSIBLE] * 2
        self.locations[Location.TOOL_MAKER].try_make_responses = [
            HasAction.WAITING_FOR_PLAYER_ACTION] * 3
        self.locations[Location.TOOL_MAKER].make_action_responses = [ActionResult.ACTION_DONE] * 2

        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        self.assertTrue(self.gpc.place_figures(self.players[1], Location.TOOL_MAKER, 1))

        state = json.loads(self.gpc.state())
        self.assertEqual(state["game phase"], "GamePhase.MAKE_ACTION")

        self.assertTrue(self.gpc.make_action(self.players[0], Location.TOOL_MAKER, [], []))
        self.assertTrue(self.gpc.make_action(self.players[0], Location.TOOL_MAKER, [], []))

    def test_making_complicated(self) -> None:
        self.mock_setup(4, [Location.TOOL_MAKER])
        self.locations[Location.TOOL_MAKER].place_responses = [True]
        self.locations[Location.TOOL_MAKER].try_place_responses = \
            [HasAction.NO_ACTION_POSSIBLE] * 4
        self.locations[Location.TOOL_MAKER].try_make_responses = [
            HasAction.WAITING_FOR_PLAYER_ACTION,  # player 0 does his first action
            HasAction.NO_ACTION_POSSIBLE,  # player 0 has no more actions, turn passes to player 1
            HasAction.WAITING_FOR_PLAYER_ACTION,  # player 1 does his first action
            HasAction.WAITING_FOR_PLAYER_ACTION,  # player 1 does his second action
            HasAction.WAITING_FOR_PLAYER_ACTION,  # player 1 does his third action
            HasAction.AUTOMATIC_ACTION_DONE,  # player 1 has done automatic action, he can do more
            HasAction.NO_ACTION_POSSIBLE,  # player 1 has no more actions, turn passes to player 2
            HasAction.WAITING_FOR_PLAYER_ACTION,  # player 1 does his third action
            HasAction.NO_ACTION_POSSIBLE,  # player 2 has no more actions, turn passes to player 3
            HasAction.NO_ACTION_POSSIBLE,  # player 3 has no actions in this mock, so turn passes
            HasAction.NO_ACTION_POSSIBLE,  # player 0 has no actions in this mock, so turn passes
            HasAction.NO_ACTION_POSSIBLE,  # player 1 has no actions in this mock, so turn passes
            HasAction.NO_ACTION_POSSIBLE,  # player 2 has no actions in this mock, so turn passes
            # now there is no action possible for each player, we move to feed tribe state
            ]
        self.locations[Location.TOOL_MAKER].make_action_responses = [ActionResult.ACTION_DONE] * 5
        self.feed_tribes[self.players[0]].is_fed_responses = [False]  # we only try to stop game
        # by waiting for player 0 to pay
        self.feed_tribes[self.players[0]].enough_responses = [False]

        self.assertTrue(self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1))
        # we change phase to MakeAction
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.MAKE_ACTION")
        self.assertTrue(self.gpc.make_action(self.players[0], Location.TOOL_MAKER, [], []))
        self.assertTrue(self.gpc.make_action(self.players[1], Location.TOOL_MAKER, [], []))
        self.assertTrue(self.gpc.make_action(self.players[1], Location.TOOL_MAKER, [], []))
        self.assertTrue(self.gpc.make_action(self.players[1], Location.TOOL_MAKER, [], []))
        self.assertTrue(self.gpc.make_action(self.players[2], Location.TOOL_MAKER, [], []))

        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.FEED_TRIBE")

    def test_new_round(self) -> None:
        # this test tries to test more than one location
        self.mock_setup(2, [Location.TOOL_MAKER, Location.BUILDING_TILE1])
        for location in self.locations:
            self.locations[location].place_responses = [True]
            self.locations[location].try_place_responses = \
                [HasAction.NO_ACTION_POSSIBLE] * 2 + [HasAction.WAITING_FOR_PLAYER_ACTION]
            self.locations[location].try_make_responses = [
                HasAction.NO_ACTION_POSSIBLE,  # to get rid of MakeAction phase
                HasAction.NO_ACTION_POSSIBLE,
            ]
            # to get into another round
            self.locations[location].new_turn_responses = [False]

        for player in self.players:
            # to get rid of FeedTribe phase:
            self.feed_tribes[player].is_fed_responses = [True]
        self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1)
        # now we should be again in place figures, because new_turn_responses are false
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.PLACE_FIGURES")

    def test_new_round_game_end(self) -> None:
        self.mock_setup(2, [Location.TOOL_MAKER, Location.BUILDING_TILE1])
        for location in self.locations:
            self.locations[location].place_responses = [True]
            self.locations[location].try_place_responses = \
                [HasAction.NO_ACTION_POSSIBLE] * 2 + [HasAction.WAITING_FOR_PLAYER_ACTION]
            self.locations[location].try_make_responses = [
                HasAction.NO_ACTION_POSSIBLE,  # to get rid of MakeAction phase
                HasAction.NO_ACTION_POSSIBLE,
            ]
            # to get into another round

        self.locations[Location.TOOL_MAKER].new_turn_responses = [False]
        self.locations[Location.BUILDING_TILE1].new_turn_responses = [True]

        for player in self.players:
            # to get rid of FeedTribe phase:
            self.feed_tribes[player].is_fed_responses = [True]
        self.gpc.place_figures(self.players[0], Location.TOOL_MAKER, 1)
        # now we are in GameEnd phase, because BUILDING_TILE1 returned True for in new round
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.GAME_END")
