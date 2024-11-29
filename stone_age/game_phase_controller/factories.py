# pylint: disable=too-many-arguments, too-many-positional-arguments
from __future__ import annotations

from typing import Mapping

from stone_age.game_phase_controller.game_phase_controller import GamePhaseController
from stone_age.game_phase_controller.place_figures_state import PlaceFiguresState
from stone_age.game_phase_controller.make_action_state import MakeActionState
from stone_age.game_phase_controller.new_round_state import NewRoundState
from stone_age.game_phase_controller.feed_tribe_state import FeedTribeState
from stone_age.game_phase_controller.waiting_for_tool_use_state import WaitingForToolUseState
from stone_age.game_phase_controller.all_players_take_a_reward_state import \
    AllPlayersTakeARewardState
from stone_age.game_phase_controller.game_end_state import GameEndState
from stone_age.game_phase_controller.simple_types import GamePhase
from stone_age.interfaces import InterfaceFigureLocation, InterfaceToolUse, \
    InterfaceTakeReward, InterfaceFeedTribe, InterfaceNewTurn, InterfaceGamePhaseController
from stone_age.simple_types import PlayerOrder, Location


def game_phase_controller_factory(places: Mapping[Location, InterfaceFigureLocation],
                                  if_tool_use: InterfaceToolUse,
                                  if_take_reward: InterfaceTakeReward,
                                  players_new_turn: Mapping[PlayerOrder, InterfaceNewTurn],
                                  players_feed_tribe: Mapping[PlayerOrder, InterfaceFeedTribe],
                                  starting_player: PlayerOrder,
                                  ) -> InterfaceGamePhaseController:
    place_figures_state = PlaceFiguresState(places)
    make_action_state = MakeActionState(places)
    new_round_state = NewRoundState(places, players_new_turn)
    feed_tribe_state = FeedTribeState(players_feed_tribe)
    waiting_for_tool_use_state = WaitingForToolUseState(if_tool_use)
    all_players_take_a_reward_state = AllPlayersTakeARewardState(
        if_take_reward)
    game_end_state = GameEndState()
    dispachers = {
        GamePhase.PLACE_FIGURES: place_figures_state,
        GamePhase.MAKE_ACTION: make_action_state,
        GamePhase.NEW_ROUND: new_round_state,
        GamePhase.FEED_TRIBE: feed_tribe_state,
        GamePhase.WAITING_FOR_TOOL_USE: waiting_for_tool_use_state,
        GamePhase.ALL_PLAYERS_TAKE_A_REWARD: all_players_take_a_reward_state,
        GamePhase.GAME_END: game_end_state,
    }
    game_phase_controller = GamePhaseController(dispachers, starting_player)
    return game_phase_controller
