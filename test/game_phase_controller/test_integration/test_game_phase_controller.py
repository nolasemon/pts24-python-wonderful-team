# pylint: disable=too-many-instance-attributes
import unittest

from typing import List, Mapping, Iterable
import json

from test.game_phase_controller.test_integration.interface_mocks import \
    LocationMock, NewTurnMock, FeedTribeMock, ToolUseMock, RewardMock
from stone_age.game_phase_controller.factories import game_phase_controller_factory
from stone_age.interfaces import InterfaceGamePhaseController
from stone_age.simple_types import Location, PlayerOrder, ActionResult, HasAction, Effect


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

    def test_waiting_for_tool_use(self) -> None:
        self.mock_setup(2, [Location.HUNTING_GROUNDS])
        self.locations[Location.HUNTING_GROUNDS].place_responses = [True]
        self.locations[Location.HUNTING_GROUNDS].try_place_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] + [HasAction.NO_ACTION_POSSIBLE] * 2
        self.locations[Location.HUNTING_GROUNDS].try_make_responses = \
            [HasAction.WAITING_FOR_PLAYER_ACTION, HasAction.NO_ACTION_POSSIBLE] * 2 + \
            [HasAction.NO_ACTION_POSSIBLE] * 2
        self.locations[Location.HUNTING_GROUNDS].make_action_responses = \
            [ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE] * 3

        self.feed_tribes[self.players[0]].is_fed_responses = [False]
        self.feed_tribes[self.players[0]].enough_responses = [False]

        self.tool_use.can_responses += [True, False] # first player can use tool once (1)
        self.tool_use.use_responses += [True] # first player uses tool (2)
        self.tool_use.can_responses += [True, True] # second player can use tools (3)
        self.tool_use.use_responses += [True] # but uses tool only once (4)
        self.tool_use.not_responses += [True] # second player finishes using tools (5)

        self.gpc.place_figures(self.players[0], Location.HUNTING_GROUNDS, 3)
        # first player places figures and the game proceeds to MakeActionState
        self.gpc.make_action(self.players[0], Location.HUNTING_GROUNDS, [], [])
        # this returns ACTION_DONE_WAIT_FOR_TOOL_USE changing the phase if the game
        self.assertEqual(json.loads(self.gpc.state())["game phase"],
                         "GamePhase.WAITING_FOR_TOOL_USE")
        # gpc tries to make automatic actions in this phase, player0 can use tools (1),
        # so WAITING_FOR_PLAYER_ACTION is returned
        self.assertTrue(self.gpc.use_tools(self.players[0], 1))
        # player0 uses tool (2), now can not use any more tools so the game returns
        # to MakeActionState, with player1 to make action
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.MAKE_ACTION")
        self.gpc.make_action(self.players[1],Location.HUNTING_GROUNDS, [], [])
        # player1 makes action, ACTION_DONE_WAIT_FOR_TOOL_USE is returned,
        # and can use tools (3) so it's GamePhase.WAITING_FOR_TOOL_USE again
        self.assertTrue(self.gpc.use_tools(self.players[1], 4))
        # player1 uses tool (4), decides not to use one again (5)
        self.assertTrue(self.gpc.no_more_tools_this_throw(self.players[1]))
        # no further actions can be done, next phase continues
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.FEED_TRIBE")

    def test_waiting_tool_use_more_players(self) -> None:
        self.mock_setup(4, [Location.HUNTING_GROUNDS])
        self.locations[Location.HUNTING_GROUNDS].place_responses = [True]
        self.locations[Location.HUNTING_GROUNDS].try_place_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] * 3 + [HasAction.NO_ACTION_POSSIBLE] * 4
        self.locations[Location.HUNTING_GROUNDS].try_make_responses = \
            [HasAction.WAITING_FOR_PLAYER_ACTION, HasAction.NO_ACTION_POSSIBLE] * 2 + \
            [HasAction.NO_ACTION_POSSIBLE] * 4
        self.locations[Location.HUNTING_GROUNDS].make_action_responses = \
            [ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE] * 4
        self.feed_tribes[self.players[0]].is_fed_responses = [False]
        self.feed_tribes[self.players[0]].enough_responses = [False]

        self.tool_use.can_responses = [False, True] * 2 # (1)
        self.tool_use.use_responses = [True] # (2)
        self.tool_use.not_responses = [True] # (3)

        self.gpc.place_figures(self.players[0], Location.HUNTING_GROUNDS, 2)
        # figures are placed and game is now in MakeActionState
        self.gpc.make_action(self.players[0], Location.HUNTING_GROUNDS, [], [])
        # this returns ACTION_DONE_WAIT_FOR_TOOL_USE, changing the game phase,
        # but try_to_make_automatic_action returns NO_ACTION_POSSIBLE,
        # because player0 cannot use tools (1)
        self.assertTrue(self.gpc.make_action(self.players[1], Location.HUNTING_GROUNDS, [], []))
        # now player1 can use tools (1)
        self.assertEqual(json.loads(self.gpc.state())["game phase"],
                         "GamePhase.WAITING_FOR_TOOL_USE")
        self.assertFalse(self.gpc.make_action(self.players[1], Location.HUNTING_GROUNDS, [], []))
        # cannot make action because of wrong GamePhase
        self.gpc.use_tools(self.players[1], 1)
        # now player1 cannot use more tools (1),
        # try_to_make_automatic_action returns NO_ACTION_POSSIBLE
        self.gpc.make_action(self.players[2], Location.HUNTING_GROUNDS, [], [])
        self.assertFalse(self.gpc.use_tools(self.players[1], 0)) # not this player's turn
        self.gpc.no_more_tools_this_throw(self.players[2])
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.FEED_TRIBE")

    def test_automatic_round(self) -> None:
        self.mock_setup(2, [Location.HUNTING_GROUNDS])
        self.locations[Location.HUNTING_GROUNDS].place_responses = [True]
        self.locations[Location.HUNTING_GROUNDS].try_place_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] + [HasAction.NO_ACTION_POSSIBLE] * 2 + \
            [HasAction.WAITING_FOR_PLAYER_ACTION]
        self.locations[Location.HUNTING_GROUNDS].try_make_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] * 2 + [HasAction.NO_ACTION_POSSIBLE] * 2
        self.locations[Location.HUNTING_GROUNDS].new_turn_responses = [False] * 2
        for player in self.players:
            self.feed_tribes[player].is_fed_responses = [False] + [True]
            self.feed_tribes[player].enough_responses = [True]

        # the first player places his figure(s) and the GPC automatically finishes the round,
        # the actions are made automatically and players' tribes fed automatically

        self.assertTrue(self.gpc.place_figures(self.players[0], Location.HUNTING_GROUNDS, 2))
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.PLACE_FIGURES")

    def test_feeding_multiple_attempts(self) -> None:
        self.mock_setup(2, [Location.HUNTING_GROUNDS])
        self.locations[Location.HUNTING_GROUNDS].place_responses = [True]
        self.locations[Location.HUNTING_GROUNDS].try_place_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] + [HasAction.NO_ACTION_POSSIBLE] * 2
        self.locations[Location.HUNTING_GROUNDS].try_make_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] * 2 + [HasAction.NO_ACTION_POSSIBLE] * 2
        self.locations[Location.HUNTING_GROUNDS].new_turn_responses = [True]

        self.feed_tribes[self.players[0]].feed_responses = [False, True]
        self.feed_tribes[self.players[0]].is_fed_responses = [False, True]
        self.feed_tribes[self.players[0]].enough_responses = [False]
        self.feed_tribes[self.players[1]].is_fed_responses = [False, True]
        self.feed_tribes[self.players[1]].enough_responses = [True]

        resources: Iterable[Effect] = []

        self.assertTrue(self.gpc.place_figures(self.players[0], Location.HUNTING_GROUNDS, 2))
        # the game should automatically proceed to FeedTribeState
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.FEED_TRIBE")
        self.assertFalse(self.gpc.feed_tribe(self.players[0], resources)) # unsuccessful attempt
        self.assertTrue(self.gpc.feed_tribe(self.players[0], resources)) # successful attempt
        # the game now proceeds to its end phase
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.GAME_END")

    def test_feeding_more_players(self) -> None:
        self.mock_setup(4, [Location.HUNTING_GROUNDS])
        self.locations[Location.HUNTING_GROUNDS].place_responses = [True]
        self.locations[Location.HUNTING_GROUNDS].try_place_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] * 3 + [HasAction.NO_ACTION_POSSIBLE] * 4 + \
            [HasAction.WAITING_FOR_PLAYER_ACTION]
        self.locations[Location.HUNTING_GROUNDS].try_make_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] * 4 + [HasAction.NO_ACTION_POSSIBLE] * 4
        self.locations[Location.HUNTING_GROUNDS].new_turn_responses = [False]

        for player in self.players:
            self.feed_tribes[player].is_fed_responses =  [False, True]
        self.feed_tribes[self.players[0]].enough_responses = [True]
        self.feed_tribes[self.players[1]].enough_responses = [False]
        self.feed_tribes[self.players[1]].not_feed_responses = [True]
        self.feed_tribes[self.players[2]].enough_responses = [True]
        self.feed_tribes[self.players[3]].enough_responses = [False]
        self.feed_tribes[self.players[3]].feed_responses = [True]

        resources: Iterable[Effect] = []

        self.gpc.place_figures(self.players[0], Location.HUNTING_GROUNDS, 2)
        # game now in FeedTribeState, but first player already fed automatically
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.FEED_TRIBE")
        self.assertTrue(self.gpc.do_not_feed_this_turn(self.players[1]))
        self.assertTrue(self.gpc.feed_tribe(self.players[3], resources))
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.PLACE_FIGURES")

    def test_reward_taking_simple(self) -> None:
        self.mock_setup(3, [Location.CIVILISATION_CARD4])
        self.locations[Location.CIVILISATION_CARD4].place_responses = [True]
        self.locations[Location.CIVILISATION_CARD4].try_place_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] * 2 + [HasAction.NO_ACTION_POSSIBLE] * 3
        self.locations[Location.CIVILISATION_CARD4].try_make_responses = \
            [HasAction.WAITING_FOR_PLAYER_ACTION] * 2
        self.locations[Location.CIVILISATION_CARD4].make_action_responses = \
            [ActionResult.ACTION_DONE_ALL_PLAYERS_TAKE_A_REWARD]

        self.reward.take_responses = [True] * 2
        self.reward.auto_responses = [
            HasAction.WAITING_FOR_PLAYER_ACTION,
            HasAction.WAITING_FOR_PLAYER_ACTION,
            HasAction.AUTOMATIC_ACTION_DONE,
            HasAction.NO_ACTION_POSSIBLE
            ]

        reward = Effect.GOLD
        self.gpc.place_figures(self.players[0], Location.CIVILISATION_CARD4, 2)
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.MAKE_ACTION")
        self.gpc.make_action(self.players[0], Location.CIVILISATION_CARD4, [], [])
        # the return value changes the GamePhase to AllPlayersTakeARewardState
        self.assertTrue(self.gpc.make_all_players_take_a_reward_choice(self.players[0], reward))
        self.assertEqual(json.loads(self.gpc.state())["game phase"],
                         "GamePhase.ALL_PLAYERS_TAKE_A_REWARD")
        self.assertFalse(self.gpc.make_all_players_take_a_reward_choice(self.players[2], reward))
        # not this player's turn
        self.assertTrue(self.gpc.make_all_players_take_a_reward_choice(self.players[1], reward))
        # the remaining player should be given the remaining reward automatically,
        # game returns to MakeActionState
        self.assertEqual(json.loads(self.gpc.state())["game phase"], "GamePhase.MAKE_ACTION")

    def test_reward_taking_wrong_order(self) -> None:
        self.mock_setup(4, [Location.CIVILISATION_CARD1])
        self.locations[Location.CIVILISATION_CARD1].place_responses = [True]
        self.locations[Location.CIVILISATION_CARD1].try_place_responses = \
            [HasAction.AUTOMATIC_ACTION_DONE] * 3 + \
            [HasAction.NO_ACTION_POSSIBLE] * 4
        self.locations[Location.CIVILISATION_CARD1].try_make_responses = \
            [HasAction.WAITING_FOR_PLAYER_ACTION]
        self.locations[Location.CIVILISATION_CARD1].make_action_responses = \
            [ActionResult.ACTION_DONE_ALL_PLAYERS_TAKE_A_REWARD]

        self.reward.auto_responses = [HasAction.WAITING_FOR_PLAYER_ACTION] * 4
        self.reward.take_responses = [True] * 3

        reward = Effect.GOLD
        self.gpc.place_figures(self.players[0], Location.CIVILISATION_CARD1, 1)
        self.gpc.make_action(self.players[0], Location.CIVILISATION_CARD1, [], [])
        self.assertTrue(self.gpc.make_all_players_take_a_reward_choice(self.players[0], reward))
        self.assertFalse(self.gpc.make_all_players_take_a_reward_choice(self.players[3], reward))
        self.assertTrue(self.gpc.make_all_players_take_a_reward_choice(self.players[1], reward))
        self.assertFalse(self.gpc.make_all_players_take_a_reward_choice(self.players[0], reward))
        self.assertTrue(self.gpc.make_all_players_take_a_reward_choice(self.players[2], reward))
        self.assertEqual(json.loads(self.gpc.state())["game phase"],
                         "GamePhase.ALL_PLAYERS_TAKE_A_REWARD")
