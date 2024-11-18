from stone_age.interfaces import InterfaceFigureLocation
from stone_age.game_board.interfaces import InterfaceFigureLocationInternal


class FigureLocationAdaptor(InterfaceFigureLocation):

    _interface_figure_location_internal: InterfaceFigureLocationInternal

    def __init__(self, interface_figure_location_internal: InterfaceFigureLocationInternal):
        assert isinstance(interface_figure_location_internal, InterfaceFigureLocationInternal)
        self._interface_figure_location_internal = interface_figure_location_internal

    @property
    def interface_figure_location_internal(self) -> InterfaceFigureLocationInternal:
        return self._interface_figure_location_internal
