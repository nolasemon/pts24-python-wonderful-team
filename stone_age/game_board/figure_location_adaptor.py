from typing import Dict, Iterable
from stone_age.simple_types import PlayerOrder, HasAction, ActionResult, Effect
from stone_age.interfaces import InterfaceFigureLocation, InterfacePlayerBoardGameBoard
from stone_age.game_board.simple_types import Player
from stone_age.game_board.interfaces import InterfaceFigureLocationInternal


class FigureLocationAdaptor(InterfaceFigureLocation):

    _interface_figure_location_internal: InterfaceFigureLocationInternal
    _dict_player_order_to_player: Dict[PlayerOrder, Player]

    def __init__(self, internal: InterfaceFigureLocationInternal,
                 dict_player_order_to_player: Dict[PlayerOrder, Player]):
        assert isinstance(internal, InterfaceFigureLocationInternal)
        self._interface_figure_location_internal: InterfaceFigureLocationInternal = internal
        self._dict_player_order_to_player: Dict[PlayerOrder, Player] = dict_player_order_to_player

    @property
    def interface_figure_location_internal(self) -> InterfaceFigureLocationInternal:
        return self._interface_figure_location_internal

    @property
    def dict_player_order_to_player(self) -> Dict[PlayerOrder, Player]:
        return self._dict_player_order_to_player

    def player_by_order(self, player_order: PlayerOrder) -> Player:
        assert isinstance(player_order, PlayerOrder)
        if player_order not in self.dict_player_order_to_player:
            self.dict_player_order_to_player[player_order] =\
                Player(player_order, InterfacePlayerBoardGameBoard())
        assert isinstance(self.dict_player_order_to_player[player_order], Player)
        return self.dict_player_order_to_player[player_order]

    def place_figures(self, player: PlayerOrder, figure_count: int) -> bool:
        assert isinstance(player, PlayerOrder) and figure_count > 0
        assert self.player_by_order(player) is not None
        return self.interface_figure_location_internal.\
            place_figures(self.player_by_order(player), figure_count)

    def try_to_place_figures(self, player: PlayerOrder, count: int) -> HasAction:
        assert isinstance(player, PlayerOrder) and count > 0
        assert self.player_by_order(player) is not None
        return self.interface_figure_location_internal.\
            try_to_place_figures(self.player_by_order(player), count)

    def make_action(self, player: PlayerOrder, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        assert all(isinstance(input_resource, Effect) for input_resource in input_resources)
        assert all(isinstance(output_resource, Effect) for output_resource in output_resources)
        assert self.player_by_order(player) is not None
        return self.interface_figure_location_internal.\
            make_action(self.player_by_order(player), input_resources, output_resources)

    def skip_action(self, player: PlayerOrder) -> bool:
        assert isinstance(player, PlayerOrder)
        assert self.player_by_order(player) is not None
        return self.interface_figure_location_internal.\
            skip_action(self.player_by_order(player))

    def try_to_make_action(self, player: PlayerOrder) -> HasAction:
        assert isinstance(player, PlayerOrder)
        assert self.player_by_order(player) is not None
        return self.interface_figure_location_internal.\
            try_to_make_action(self.player_by_order(player))

    def new_turn(self) -> bool:
        return self.interface_figure_location_internal.new_turn()
