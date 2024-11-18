from stone_age.simple_types import HasAction
from stone_age.game_board.simple_types import Player
from stone_age.game_board.interfaces import InterfaceFigureLocationInternal
from stone_age.game_board.tool_maker_hut_fields import ToolMakerHutFields


class PlaceOnToolMakerAdaptor(InterfaceFigureLocationInternal):
    _tool_maker: ToolMakerHutFields

    def __init__(self, tool_maker: ToolMakerHutFields):
        assert isinstance(tool_maker, ToolMakerHutFields)
        self._tool_maker: ToolMakerHutFields = tool_maker

    def place_figures(self, player: Player, figure_count: int) -> bool:
        assert isinstance(player, Player) and figure_count > 0
        if self.try_to_place_figures(player, figure_count) == HasAction.NO_ACTION_POSSIBLE:
            return False
        self._tool_maker.place_on_tool_maker(player)
        return True

    def try_to_place_figures(self, player: Player, count: int) -> HasAction:
        """If a figure will be placed, action will be done automatically"""
        assert isinstance(player, Player) and count > 0
        if not player.player_board.has_figures(count):
            return HasAction.NO_ACTION_POSSIBLE
        if count > 1:
            return HasAction.NO_ACTION_POSSIBLE
        if not self._tool_maker.can_place_on_tool_maker(player):
            return HasAction.NO_ACTION_POSSIBLE
        return HasAction.AUTOMATIC_ACTION_DONE

    def new_turn(self) -> bool:
        """It is no way, that the tool maker location implies end of the game"""
        return False