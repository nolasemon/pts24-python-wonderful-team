from typing import Iterable

from stone_age.simple_types import PlayerOrder
from stone_age.interfaces import InterfacePlayerBoardGameBoard
from stone_age.simple_types import EndOfGameEffect, ImmediateEffect

class Player:
    _player_order: PlayerOrder
    _player_board: InterfacePlayerBoardGameBoard

    def __init__(self, player_order: PlayerOrder, player_board: InterfacePlayerBoardGameBoard):
        assert isinstance(player_order, PlayerOrder)
        assert isinstance(player_board, InterfacePlayerBoardGameBoard)
        self._player_order = player_order
        self._player_board = player_board

    @property
    def player_order(self) -> PlayerOrder:
        return self._player_order

    @property
    def player_board(self) -> InterfacePlayerBoardGameBoard:
        return self._player_board

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self._player_order == other.player_order and self._player_board == other.player_board


class CivilizationCard:

    def __init__(self, effect_type: Iterable[ImmediateEffect],
                 end_of_game_eff: Iterable[EndOfGameEffect]) -> None:
        self.immediate_effect: list[ImmediateEffect] = list(effect_type)
        self.end_of_game_effect: list[EndOfGameEffect] = list(end_of_game_eff)
