from typing import List
from stone_age.simple_types import Effect, HasAction, PlayerOrder


class AllPlayersTakeReward:
    def __init__(self) -> None:
        self._menu: List[Effect] = []
        self._players: List[PlayerOrder] = []
        self._current_player_index: int = 0

    @property
    def menu(self) -> List[Effect]:
        return self._menu

    @property
    def players(self) -> List[PlayerOrder]:
        return self._players

    @property
    def current_player_index(self) -> int:
        return self._current_player_index

    def initiate(self, menu: List[Effect], players: List[PlayerOrder]) -> None:
        self._menu = menu.copy()
        self._players = players
        self._current_player_index = 0

    def try_make_action(self, player: PlayerOrder) -> HasAction:
        if not self._menu:
            return HasAction.NO_ACTION_POSSIBLE

        if player != self._players[self._current_player_index]:
            return HasAction.NO_ACTION_POSSIBLE

        return HasAction.WAITING_FOR_PLAYER_ACTION

    def take_reward(self, player: PlayerOrder, reward: Effect) -> bool:
        if not self._menu:
            return False

        if player != self._players[self._current_player_index]:
            return False

        if reward not in self._menu:
            return False

        self._menu.remove(reward)
        self._current_player_index = (
            self._current_player_index + 1) % len(self._players)
        return True

    def state(self) -> str:
        return (
            f"Menu: {self._menu}, Players: {self._players}, "
            f"Current Player Index: {self._current_player_index}"
        )
