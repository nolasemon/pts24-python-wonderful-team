from stone_age.simple_types import PlayerOrder
from stone_age.interfaces import InterfaceFigureLocation
from stone_age.game_board.simple_types import Player
from stone_age.game_board.interfaces import InterfaceFigureLocationInternal

class FigureLocationAdaptor(InterfaceFigureLocation):

    _interface_figure_location_internal: InterfaceFigureLocationInternal
    _player: Player

    def __init__(self, interface_figure_location_internal: InterfaceFigureLocationInternal):
        assert isinstance(interface_figure_location_internal, InterfaceFigureLocationInternal)
        self._interface_figure_location_internal = interface_figure_location_internal

    def place_figures(self, player: PlayerOrder, figureCount: int) -> bool:
        assert isinstance(player, Player) and figureCount > 0
        return self._interface_figure_location_internal.place_figures(player, figureCount)

