from typing import Iterable
from stone_age.game_board.interfaces import InterfaceRewardMenu
from stone_age.simple_types import Effect, PlayerOrder, HasAction


class RewardMenu(InterfaceRewardMenu):
    def initiate(self, rewards: Iterable[Effect]) -> None:
        pass

    def take_reward(self, player: PlayerOrder, reward: Effect) -> bool:
        return False

    def try_make_action(self, player: PlayerOrder) -> HasAction:
        return HasAction.NO_ACTION_POSSIBLE
