from __future__ import annotations
from typing import Iterable, Mapping, Optional, Any
import json

from stone_age.interfaces import InterfaceGamePhaseController
from stone_age.simple_types import PlayerOrder, Location, Effect, ActionResult, HasAction
from stone_age.game_phase_controller.interfaces import InterfaceGamePhaseState
from stone_age.game_phase_controller.simple_types import GamePhase


class GamePhaseController(InterfaceGamePhaseController):
    _dispatchers: Mapping[GamePhase, InterfaceGamePhaseState]
    _round_starting_player: PlayerOrder
    _current_player: PlayerOrder
    _current_player_taking_reward: Optional[PlayerOrder]
    _game_phase: GamePhase

    def __init__(self, dispatchers: Mapping[GamePhase, InterfaceGamePhaseState],
                 starting_player: PlayerOrder):
        self._round_starting_player = starting_player
        self._current_player = starting_player
        self._current_player_taking_reward = None
        self._dispatchers = dict(dispatchers)
        self._game_phase = GamePhase.PLACE_FIGURES

    def _check_players_turn(self, player: PlayerOrder) -> bool:
        match self._game_phase:
            case GamePhase.PLACE_FIGURES | GamePhase.MAKE_ACTION | GamePhase.WAITING_FOR_TOOL_USE:
                return player == self._current_player
            case GamePhase.ALL_PLAYERS_TAKE_A_REWARD:
                assert self._current_player_taking_reward is not None
                return player == self._current_player_taking_reward
            case GamePhase.FEED_TRIBE:
                return True
            case GamePhase.NEW_ROUND:
                return False
            case _:  # GAME_END
                assert False

    def _progress_state_after_succesfull_action(self) -> None:
        match self._game_phase:
            case GamePhase.PLACE_FIGURES | GamePhase.FEED_TRIBE:
                self._current_player = self._current_player.forward()
                return
            case GamePhase.MAKE_ACTION | GamePhase.WAITING_FOR_TOOL_USE:
                return
            case GamePhase.ALL_PLAYERS_TAKE_A_REWARD:
                assert self._current_player_taking_reward is not None
                self._current_player_taking_reward = self._current_player_taking_reward.forward()
                return
            case GamePhase.NEW_ROUND:
                self._game_phase = GamePhase.PLACE_FIGURES
                self._round_starting_player = self._round_starting_player.forward()
                self._current_player = self._round_starting_player
            case _:  # GAME_END
                assert False

    def _progress_state_after_no_action_possible(self) -> None:
        match self._game_phase:
            case GamePhase.PLACE_FIGURES | GamePhase.FEED_TRIBE | GamePhase.MAKE_ACTION:
                self._current_player = self._current_player.forward()
                return
            case GamePhase.ALL_PLAYERS_TAKE_A_REWARD | GamePhase.WAITING_FOR_TOOL_USE:
                self._current_player_taking_reward = None
                self._game_phase = GamePhase.MAKE_ACTION
                return
            case GamePhase.NEW_ROUND:
                self._game_phase = GamePhase.GAME_END
                return
            case _:  # GAME_END
                assert False

    def _progress_state_after_no_action_possible_by_any_player(self) -> None:
        match self._game_phase:
            case GamePhase.PLACE_FIGURES:
                self._current_player = self._round_starting_player
                self._game_phase = GamePhase.MAKE_ACTION
                return
            case GamePhase.MAKE_ACTION:
                self._current_player = self._round_starting_player
                self._game_phase = GamePhase.FEED_TRIBE
                return
            case GamePhase.FEED_TRIBE:
                self._current_player = self._round_starting_player
                self._game_phase = GamePhase.NEW_ROUND
            case _:  # NEW_ROUND, WAITING_FOR_TOOL_USE, ALL_PLAYERS_TAKE_A_REWARD, GAME_END
                assert False

    def _progress_state_tool_use(self) -> None:
        match self._game_phase:
            case GamePhase.MAKE_ACTION:
                self._game_phase = GamePhase.WAITING_FOR_TOOL_USE
                return
            case _:
                assert False

    def _progress_state_all_players_take_a_reward(self) -> None:
        match self._game_phase:
            case GamePhase.MAKE_ACTION:
                self._game_phase = GamePhase.ALL_PLAYERS_TAKE_A_REWARD
                self._current_player_taking_reward = self._current_player
                return
            case _:
                assert False

    def _try_to_do_further_actions(self) -> None:
        first_unsuccesful_player: Optional[PlayerOrder] = None
        while True:
            dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
            player: PlayerOrder = self._current_player_taking_reward or self._current_player
            if self._game_phase != GamePhase.GAME_END and first_unsuccesful_player == player:
                self._progress_state_after_no_action_possible_by_any_player()
                first_unsuccesful_player = None
                continue
            action_result: HasAction = dispatcher.try_to_make_automatic_action(
                player)
            match action_result:
                case HasAction.WAITING_FOR_PLAYER_ACTION:
                    first_unsuccesful_player = None
                    return
                case HasAction.AUTOMATIC_ACTION_DONE:
                    first_unsuccesful_player = None
                    self._progress_state_after_succesfull_action()
                case HasAction.NO_ACTION_POSSIBLE:
                    if first_unsuccesful_player is None:
                        first_unsuccesful_player = player
                    self._progress_state_after_no_action_possible()
                    continue
                case _:
                    assert False

    def place_figures(self, player: PlayerOrder, location: Location, figures_count: int) -> bool:
        if not self._check_players_turn(player):
            return False
        dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
        action_result: ActionResult = dispatcher.place_figures(
            player, location, figures_count)
        match action_result:
            case ActionResult.FAILURE:
                return False
            case ActionResult.ACTION_DONE:
                self._progress_state_after_succesfull_action()
                self._try_to_do_further_actions()
                return True
            case _:
                assert False

    def make_action(self, player: PlayerOrder, location: Location,
                    input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> bool:
        if not self._check_players_turn(player):
            return False
        dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
        action_result: ActionResult = dispatcher.make_action(
            player, location, input_resources, output_resources)
        match action_result:
            case ActionResult.FAILURE:
                return False
            case ActionResult.ACTION_DONE:
                self._progress_state_after_succesfull_action()
                self._try_to_do_further_actions()
                return True
            case ActionResult.ACTION_DONE_WAIT_FOR_TOOL_USE:
                self._progress_state_tool_use()
                self._try_to_do_further_actions()
                return True
            case ActionResult.ACTION_DONE_ALL_PLAYERS_TAKE_A_REWARD:
                self._progress_state_all_players_take_a_reward()
                self._try_to_do_further_actions()
                return True
            case _:
                assert False

    def skip_action(self, player: PlayerOrder, location: Location) -> bool:
        if not self._check_players_turn(player):
            return False
        dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
        action_result: ActionResult = dispatcher.skip_action(player, location)
        match action_result:
            case ActionResult.FAILURE:
                return False
            case ActionResult.ACTION_DONE:
                self._progress_state_after_succesfull_action()
                self._try_to_do_further_actions()
                return True
            case _:
                assert False

    def use_tools(self, player: PlayerOrder, tool_index: int) -> bool:
        if not self._check_players_turn(player):
            return False
        dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
        action_result: ActionResult = dispatcher.use_tools(player, tool_index)
        match action_result:
            case ActionResult.FAILURE:
                return False
            case ActionResult.ACTION_DONE:
                self._progress_state_after_succesfull_action()
                self._try_to_do_further_actions()
                return True
            case _:
                assert False

    def no_more_tools_this_throw(self, player: PlayerOrder) -> bool:
        if not self._check_players_turn(player):
            return False
        dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
        action_result: ActionResult = dispatcher.no_more_tools_this_throw(
            player)
        match action_result:
            case ActionResult.FAILURE:
                return False
            case ActionResult.ACTION_DONE:
                self._progress_state_after_no_action_possible()
                self._try_to_do_further_actions()
                return True
            case _:
                assert False

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> bool:
        if not self._check_players_turn(player):
            return False
        dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
        action_result: ActionResult = dispatcher.feed_tribe(player, resources)
        match action_result:
            case ActionResult.FAILURE:
                return False
            case ActionResult.ACTION_DONE:
                self._progress_state_after_succesfull_action()
                self._try_to_do_further_actions()
                return True
            case _:
                assert False

    def do_not_feed_this_turn(self, player: PlayerOrder) -> bool:
        if not self._check_players_turn(player):
            return False
        dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
        action_result: ActionResult = dispatcher.do_not_feed_this_turn(player)
        match action_result:
            case ActionResult.FAILURE:
                return False
            case ActionResult.ACTION_DONE:
                self._progress_state_after_succesfull_action()
                self._try_to_do_further_actions()
                return True
            case _:
                assert False

    def make_all_players_take_a_reward_choice(self, player: PlayerOrder, reward: Effect) -> bool:
        if not self._check_players_turn(player):
            return False
        dispatcher: InterfaceGamePhaseState = self._dispatchers[self._game_phase]
        action_result: ActionResult = dispatcher.make_all_players_take_a_reward_choice(
            player, reward)
        match action_result:
            case ActionResult.FAILURE:
                return False
            case ActionResult.ACTION_DONE:
                self._progress_state_after_succesfull_action()
                self._try_to_do_further_actions()
                return True
            case _:
                assert False

    def state(self) -> str:
        state: Any = {
            "game phase": str(self._game_phase),
            "round starting player": self._round_starting_player.order,
            "current_player": self._current_player.order,
            "player taking a reward": "None" if self._current_player_taking_reward is None
            else self._current_player_taking_reward.order
        }
        return json.dumps(state)
