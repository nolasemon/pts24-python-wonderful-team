from __future__ import annotations
from typing import List, Iterable
from stone_age.simple_types import Effect, ActionResult
from stone_age.game_board.simple_types import Player
from stone_age.game_board.reward_menu import RewardMenu
from stone_age.game_board.interfaces import EvaluateCivilizationCardImmediateEffect, InterfaceThrow


class AllPlayersTakeReward(EvaluateCivilizationCardImmediateEffect):
    def __init__(self, reward_menu: RewardMenu, throw: InterfaceThrow) -> None:
        self._reward_menu = reward_menu
        self._throw = throw

    def perform_effect(self, player: Player, choice: Iterable[Effect]) -> ActionResult:
        number_of_players = player.player_order.players
        rewards: List[Effect] = []
        for _ in range(number_of_players):
            rewards.append(Effect(self._throw.throw(1)[0]))

        self._reward_menu.initiate(rewards)
        return ActionResult.ACTION_DONE_ALL_PLAYERS_TAKE_A_REWARD
