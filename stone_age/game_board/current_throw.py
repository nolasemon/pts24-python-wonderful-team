from stone_age.game_board.interfaces import InterfaceCurrentThrow
from stone_age.simple_types import Effect
from stone_age.game_board.simple_types import Player


class CurrentThrow(InterfaceCurrentThrow):
    def initiate(self, player: Player, choice: Effect, dices: int) -> None:
        pass
