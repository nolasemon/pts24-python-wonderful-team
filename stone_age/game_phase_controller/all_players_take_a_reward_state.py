from __future__ import annotations

from stone_age.game_phase_controller.interfaces import GamePhaseStateFailureMeta
from stone_age.interfaces import InterfaceTakeReward
from stone_age.simple_types import PlayerOrder, Effect, HasAction, ActionResult


class AllPlayersTakeARewardState(GamePhaseStateFailureMeta):
    _interface_take_reward: InterfaceTakeReward

    def __init__(self, interface_take_reward: InterfaceTakeReward):
        self._interface_take_reward = interface_take_reward

    def make_all_players_take_a_reward_choice(self, player: PlayerOrder,
                                              reward: Effect) -> ActionResult:
        if self._interface_take_reward.take_reward(player, reward):
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        return self._interface_take_reward.try_make_action(player)
