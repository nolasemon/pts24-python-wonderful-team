import json
from typing import List, Any, Mapping
from stone_age.simple_types import Effect, HasAction, PlayerOrder
from stone_age.game_board.simple_types import Player
from stone_age.interfaces import InterfaceTakeReward


class RewardMenu(InterfaceTakeReward):
    def __init__(self,
                 players: Mapping[PlayerOrder, Player]) -> None:
        self.menu: List[Effect] = []
        self.players = players

    def initiate(self, menu: List[Effect]) -> None:
        self.menu = menu

    def take_reward(self, player: PlayerOrder, reward: Effect) -> bool:
        if reward in self.menu:
            self.players[player].player_board.give_effect([reward])
            self.menu.remove(reward)
            return True
        return False

    def try_make_action(self, player: PlayerOrder) -> HasAction:
        if len(self.menu) == 1:
            self.players[player].player_board.give_effect(self.menu)
            self.menu.pop()
            return HasAction.AUTOMATIC_ACTION_DONE
        if len(self.menu) > 1:
            return HasAction.WAITING_FOR_PLAYER_ACTION
        return HasAction.NO_ACTION_POSSIBLE

    def state(self) -> str:
        state: Any = {
            "menu content": [effect.name for effect in self.menu]
        }
        return json.dumps(state)
