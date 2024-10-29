# pylint: disable=too-many-instance-attributes
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

    def state_string(self) -> str:
        state: Any = json.loads(self.controller.state())
        return str(state["game phase"])+","+str(state["round starting player"])+"/" \
            + str(state["current_player"])+"/" + \
            str(state["player taking a reward"])

    def test_players_swap_as_expected(self) -> None:
        self.assertEqual(self.state_string(),
                         "GamePhase.PLACE_FIGURES,0/0/None")

        # incorrect player
        res = self.controller.place_figures(
            PlayerOrder(1, 2), Location.BUILDING_TILE1, 1)
        self.assertFalse(res)
        self.assertEqual(self.state_string(),
                         "GamePhase.PLACE_FIGURES,0/0/None")

        # correct player succesfully places figure
        self.place_figures_state.expected_action_results.append(
            ActionResult.ACTION_DONE)
        self.place_figures_state.expected_has_action.append(
            HasAction.WAITING_FOR_PLAYER_ACTION)
        res = self.controller.place_figures(
            PlayerOrder(0, 2), Location.BUILDING_TILE1, 1)
        self.assertTrue(res)
        self.assertEqual(self.state_string(),
                         "GamePhase.PLACE_FIGURES,0/1/None")

        # correct player succesfully places figure, next player has no action, but another one has
        self.place_figures_state.expected_action_results.append(
            ActionResult.ACTION_DONE)
        self.place_figures_state.expected_has_action.append(
            HasAction.NO_ACTION_POSSIBLE)
        self.place_figures_state.expected_has_action.append(
            HasAction.WAITING_FOR_PLAYER_ACTION)
        res = self.controller.place_figures(
            PlayerOrder(1, 2), Location.BUILDING_TILE1, 1)
        self.assertTrue(res)
        self.assertEqual(self.state_string(),
                         "GamePhase.PLACE_FIGURES,0/1/None")

        # correct player succesfully places figure, but nobody has an action
        self.place_figures_state.expected_action_results.append(
            ActionResult.ACTION_DONE)
        self.place_figures_state.expected_has_action.append(
            HasAction.NO_ACTION_POSSIBLE)
        self.place_figures_state.expected_has_action.append(
            HasAction.NO_ACTION_POSSIBLE)
        self.make_action_state.expected_has_action.append(
            HasAction.WAITING_FOR_PLAYER_ACTION)
        res = self.controller.place_figures(
            PlayerOrder(1, 2), Location.BUILDING_TILE1, 1)
        self.assertTrue(res)
        self.assertEqual(self.state_string(), "GamePhase.MAKE_ACTION,0/0/None")

        # action evaluation does not swap who is on turn
        self.make_action_state.expected_action_results.append(
            ActionResult.ACTION_DONE)
        self.make_action_state.expected_has_action.append(
            HasAction.WAITING_FOR_PLAYER_ACTION)
        res = self.controller.make_action(
            PlayerOrder(0, 2), Location.BUILDING_TILE1, [], [])
        self.assertTrue(res)
        self.assertEqual(self.state_string(), "GamePhase.MAKE_ACTION,0/0/None")

        # move to feed tribe phase
        self.make_action_state.expected_action_results.append(
            ActionResult.ACTION_DONE)
        self.make_action_state.expected_has_action.append(
            HasAction.NO_ACTION_POSSIBLE)
        self.make_action_state.expected_has_action.append(
            HasAction.NO_ACTION_POSSIBLE)
        self.feed_tribe_state.expected_has_action.append(
            HasAction.WAITING_FOR_PLAYER_ACTION)
        res = self.controller.make_action(
            PlayerOrder(0, 2), Location.BUILDING_TILE1, [], [])
        self.assertTrue(res)
        self.assertEqual(self.state_string(), "GamePhase.FEED_TRIBE,0/0/None")

        # order in Feed trib phase is arbitrary, move to new turm and game ends
        self.feed_tribe_state.expected_action_results.append(
            ActionResult.ACTION_DONE)
        self.feed_tribe_state.expected_has_action.append(
            HasAction.NO_ACTION_POSSIBLE)
        self.feed_tribe_state.expected_has_action.append(
            HasAction.NO_ACTION_POSSIBLE)
        self.new_round_state.expected_has_action.append(
            HasAction.NO_ACTION_POSSIBLE)  # indicates game end
        self.game_end_state.expected_has_action.append(
            HasAction.WAITING_FOR_PLAYER_ACTION)
        res = self.controller.feed_tribe(PlayerOrder(1, 2), [])
        self.assertTrue(res)
        self.assertEqual(self.state_string(), "GamePhase.GAME_END,0/0/None")


if __name__ == "__main__":
    unittest.main()
