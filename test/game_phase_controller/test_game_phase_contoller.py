# pylint: disable=too-many-instance-attributes, too-many-public-methods
from typing import Iterable, Any
import unittest
import json
from stone_age.game_phase_controller.game_phase_controller import GamePhaseController
from stone_age.game_phase_controller.interfaces import InterfaceGamePhaseState
from stone_age.game_phase_controller.simple_types import GamePhase
from stone_age.simple_types import ActionResult, HasAction, PlayerOrder, Location, Effect


class StateMock(InterfaceGamePhaseState):
    expected_action_results: list[ActionResult]
    expected_has_action: list[HasAction]

    def __init__(self) -> None:
        self.expected_action_results = []
        self.expected_has_action = []

    def place_figures(self, player: PlayerOrder, location: Location,
                      figures_count: int) -> ActionResult:
        assert self.expected_action_results
        return self.expected_action_results.pop(0)

    def make_action(self, player: PlayerOrder, location: Location,
                    input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert self.expected_action_results
        return self.expected_action_results.pop(0)

    def skip_action(self, player: PlayerOrder, location: Location) -> ActionResult:
        assert self.expected_action_results
        return self.expected_action_results.pop(0)

    def use_tools(self, player: PlayerOrder, tool_index: int) -> ActionResult:
        assert self.expected_action_results
        return self.expected_action_results.pop(0)

    def no_more_tools_this_throw(self, player: PlayerOrder) -> ActionResult:
        assert self.expected_action_results
        return self.expected_action_results.pop(0)

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> ActionResult:
        assert self.expected_action_results
        return self.expected_action_results.pop(0)

    def do_not_feed_this_turn(self, player: PlayerOrder) -> ActionResult:
        assert self.expected_action_results
        return self.expected_action_results.pop(0)

    def make_all_players_take_a_reward_choice(self, player: PlayerOrder,
                                              reward: Effect) -> ActionResult:
        assert self.expected_action_results
        return self.expected_action_results.pop(0)

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        assert self.expected_has_action
        return self.expected_has_action.pop(0)


class TestGamePhaseController(unittest.TestCase):
    def setUp(self) -> None:
        self.place_figures_state: StateMock = StateMock()
        self.make_action_state: StateMock = StateMock()
        self.feed_tribe_state: StateMock = StateMock()
        self.new_round_state: StateMock = StateMock()
        self.waiting_for_tool_use_state: StateMock = StateMock()
        self.all_players_take_a_reward_state: StateMock = StateMock()
        self.game_end_state: StateMock = StateMock()

        dispatchers = {
            GamePhase.PLACE_FIGURES: self.place_figures_state,
            GamePhase.MAKE_ACTION: self.make_action_state,
            GamePhase.FEED_TRIBE: self.feed_tribe_state,
            GamePhase.NEW_ROUND: self.new_round_state,
            GamePhase.WAITING_FOR_TOOL_USE: self.waiting_for_tool_use_state,
            GamePhase.ALL_PLAYERS_TAKE_A_REWARD: self.all_players_take_a_reward_state,
            GamePhase.GAME_END: self.game_end_state,
        }

        self.controller = GamePhaseController(
            dispatchers, PlayerOrder(0, 2))

    def check_state_string(self, expected_string: str) -> None:
        state: Any = json.loads(self.controller.state())
        state_string: str = str(state["game phase"])+","+str(state["round starting player"])+"/" \
            + str(state["current_player"])+"/" + \
            str(state["player taking a reward"])
        self.assertEqual(expected_string, state_string)

    def mock_setup(self, description: str) -> None:
        """Uses strings like "pDAW mNN" to set up mocks."""
        for part in description.split():
            mock: StateMock
            match part[0]:
                case 'p':
                    mock = self.place_figures_state
                case 'm':
                    mock = self.make_action_state
                case 'f':
                    mock = self.feed_tribe_state
                case 'n':
                    mock = self.new_round_state
                case 'g':
                    mock = self.game_end_state
                case 'w':
                    mock = self.waiting_for_tool_use_state
                case 'a':
                    mock = self.all_players_take_a_reward_state
                case _:
                    assert False
            for char in part[1:]:
                match char:
                    case 'A':
                        mock.expected_has_action.append(
                            HasAction.AUTOMATIC_ACTION_DONE)
                    case 'N':
                        mock.expected_has_action.append(
                            HasAction.NO_ACTION_POSSIBLE)
                    case 'W':
                        mock.expected_has_action.append(
                            HasAction.WAITING_FOR_PLAYER_ACTION)
                    case 'F':
                        mock.expected_action_results.append(
                            ActionResult.FAILURE)
                    case 'D':
                        mock.expected_action_results.append(
                            ActionResult.ACTION_DONE)
                    case 'R':
                        mock.expected_action_results.append(
                            ActionResult.ACTION_DONE_ALL_PLAYERS_TAKE_A_REWARD)
                    case 'T':
                        mock.expected_action_results.append(
                            ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE)
                    case _:
                        assert False

    def place_figures(self, idx1: int, idx2: int = 2) -> bool:
        return self.controller.place_figures(PlayerOrder(idx1, idx2), Location.BUILDING_TILE1, 1)

    def make_action(self, idx1: int, idx2: int = 2) -> bool:
        return self.controller.make_action(PlayerOrder(idx1, idx2),
                                           Location.BUILDING_TILE1, [], [])

    def feed_tribe(self, idx1: int, idx2: int = 2) -> bool:
        return self.controller.feed_tribe(PlayerOrder(idx1, idx2), [])

    def use_tools(self, idx1: int, idx2: int = 2) -> bool:
        return self.controller.use_tools(PlayerOrder(idx1, idx2), 1)

    def no_more_tools_this_throw(self, idx1: int, idx2: int = 2) -> bool:
        return self.controller.no_more_tools_this_throw(PlayerOrder(idx1, idx2))

    def make_all_players_take_a_reward_choice(self, idx1: int, idx2: int = 2) -> bool:
        return self.controller.make_all_players_take_a_reward_choice(PlayerOrder(idx1, idx2),
                                                                     Effect.WOOD)

    def test_starting_state(self) -> None:
        self.check_state_string("GamePhase.PLACE_FIGURES,0/0/None")

    def test_incorrect_player_tried_to_take_turn(self) -> None:
        self.assertFalse(self.place_figures(1))
        self.check_state_string("GamePhase.PLACE_FIGURES,0/0/None")

    def test_incorrect_player_order_object_failure(self) -> None:
        self.assertRaises(AssertionError, self.place_figures, 0, 3)

    def test_players_swapping_placing_figures(self) -> None:
        self.mock_setup("pDW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.PLACE_FIGURES,0/1/None")

        self.mock_setup("pDNW")
        self.assertTrue(self.place_figures(1))
        self.check_state_string("GamePhase.PLACE_FIGURES,0/1/None")

        self.mock_setup("pDNN mW")
        self.assertTrue(self.place_figures(1))
        self.check_state_string("GamePhase.MAKE_ACTION,0/0/None")

    def test_correct_player_starts_making_action(self) -> None:
        self.mock_setup("pDW")
        self.assertTrue(self.place_figures(0))
        self.mock_setup("pDNN mW")
        self.assertTrue(self.place_figures(1))
        self.check_state_string("GamePhase.MAKE_ACTION,0/0/None")

    def test_players_swapping_making_action(self) -> None:
        self.mock_setup("pDNN mW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/0/None")

        self.mock_setup("mDW")
        self.assertTrue(self.make_action(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/0/None")

        self.mock_setup("mF")
        self.assertFalse(self.make_action(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/0/None")

        self.mock_setup("mDNW")
        self.assertTrue(self.make_action(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/1/None")

        self.mock_setup("mDW")
        self.assertTrue(self.make_action(1))
        self.check_state_string("GamePhase.MAKE_ACTION,0/1/None")

        self.mock_setup("mDNN fW")
        self.assertTrue(self.make_action(1))
        self.check_state_string("GamePhase.FEED_TRIBE,0/0/None")

    def test_feed_tribe_on_and_out_of_order(self) -> None:
        self.mock_setup("pDNN mNN fW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.FEED_TRIBE,0/0/None")

        self.mock_setup("fDW")
        self.assertTrue(self.feed_tribe(1))
        self.check_state_string("GamePhase.FEED_TRIBE,0/1/None")

        self.mock_setup("fDNAW")
        self.assertTrue(self.feed_tribe(1))
        self.check_state_string("GamePhase.FEED_TRIBE,0/0/None")

    def test_next_turn(self) -> None:
        self.mock_setup("pDNN mNN fNN nA pW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.PLACE_FIGURES,1/1/None")

    def test_game_end(self) -> None:
        self.mock_setup("pDNN mNN fNN nN gW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.GAME_END,0/0/None")

    def test_tool_use_forced_stop(self) -> None:
        self.mock_setup("pDNN mW")
        self.assertTrue(self.place_figures(0))

        self.mock_setup("mT wW")  # make action - WAITING_FOR_TOOL_USE
        self.assertTrue(self.make_action(0))
        self.check_state_string("GamePhase.WAITING_FOR_TOOL_USE,0/0/None")

        self.mock_setup("wF")
        self.assertFalse(self.use_tools(0))
        self.check_state_string("GamePhase.WAITING_FOR_TOOL_USE,0/0/None")

        self.mock_setup("wDW")
        self.assertTrue(self.use_tools(0))
        self.check_state_string("GamePhase.WAITING_FOR_TOOL_USE,0/0/None")

        self.mock_setup("wDN mW")
        self.assertTrue(self.use_tools(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/0/None")

    def test_tool_use_decided_to_stop(self) -> None:
        self.mock_setup("pDNN mNW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/1/None")

        self.mock_setup("mT wW")
        self.assertTrue(self.make_action(1))
        self.check_state_string("GamePhase.WAITING_FOR_TOOL_USE,0/1/None")

        self.mock_setup("wDW")
        self.assertTrue(self.use_tools(1))
        self.check_state_string("GamePhase.WAITING_FOR_TOOL_USE,0/1/None")

        self.mock_setup("wD mW")  # done no more tools
        self.assertTrue(self.no_more_tools_this_throw(1))
        self.check_state_string("GamePhase.MAKE_ACTION,0/1/None")

    def test_all_players_take_a_reward(self) -> None:
        self.mock_setup("pDNN mNW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/1/None")

        self.mock_setup("mR aW")
        self.assertTrue(self.make_action(1))
        self.check_state_string("GamePhase.ALL_PLAYERS_TAKE_A_REWARD,0/1/1")

        self.mock_setup("aF")
        self.assertFalse(self.make_all_players_take_a_reward_choice(1))
        self.check_state_string("GamePhase.ALL_PLAYERS_TAKE_A_REWARD,0/1/1")

        self.assertFalse(self.make_all_players_take_a_reward_choice(0))
        self.check_state_string("GamePhase.ALL_PLAYERS_TAKE_A_REWARD,0/1/1")

        self.mock_setup("aDW")
        self.assertTrue(self.make_all_players_take_a_reward_choice(1))
        self.check_state_string("GamePhase.ALL_PLAYERS_TAKE_A_REWARD,0/1/0")

        self.mock_setup("aDW")
        self.assertTrue(self.make_all_players_take_a_reward_choice(0))
        self.check_state_string("GamePhase.ALL_PLAYERS_TAKE_A_REWARD,0/1/1")

        self.mock_setup("aDAW")
        self.assertTrue(self.make_all_players_take_a_reward_choice(1))
        self.check_state_string("GamePhase.ALL_PLAYERS_TAKE_A_REWARD,0/1/1")

        self.mock_setup("aDN mW")
        self.assertTrue(self.make_all_players_take_a_reward_choice(1))
        self.check_state_string("GamePhase.MAKE_ACTION,0/1/None")

    def test_no_tools_last_action(self) -> None:
        self.mock_setup("pDNN mW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/0/None")

        self.mock_setup("mT wN mNN fW")
        self.assertTrue(self.make_action(0))
        self.check_state_string("GamePhase.FEED_TRIBE,0/0/None")

    def test_all_players_take_a_reward_last_action(self) -> None:
        self.mock_setup("pDNN mW")
        self.assertTrue(self.place_figures(0))
        self.check_state_string("GamePhase.MAKE_ACTION,0/0/None")

        self.mock_setup("mR aN mNN fW")
        self.assertTrue(self.make_action(0))
        self.check_state_string("GamePhase.FEED_TRIBE,0/0/None")


if __name__ == "__main__":
    unittest.main()
