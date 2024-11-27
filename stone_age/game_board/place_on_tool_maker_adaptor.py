from typing import Iterable
from stone_age.simple_types import HasAction, Effect, ActionResult
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
        """
        If a figure can be placed, we wait for a player, otherwise there is
        no action possible.
        """
        assert isinstance(player, Player) and count > 0
        if count > 1:
            return HasAction.NO_ACTION_POSSIBLE
        if not self._tool_maker.can_place_on_tool_maker(player):
            return HasAction.NO_ACTION_POSSIBLE
        return HasAction.WAITING_FOR_PLAYER_ACTION


    def make_action(self, player: Player, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        """
        The player needs neither input nor output resources to make an action on the tool maker.
        After the action location must be clear and prepared for a new turn.
        """
        assert isinstance(player, Player)
        assert all(isinstance(effect, Effect) for effect in input_resources)
        assert all(isinstance(effect, Effect) for effect in output_resources)
        if input_resources:
            return ActionResult.FAILURE
        if output_resources:
            return ActionResult.FAILURE
        if not self._tool_maker.action_tool_maker(player):
            return ActionResult.FAILURE
        self._tool_maker.new_turn()
        return ActionResult.ACTION_DONE

    def skip_action(self, player: Player) -> bool:
        """It is no way, that player can take her figure and leave tht tool maker in place"""
        return False

    def try_to_make_action(self, player: Player) -> HasAction:
        """If action can be made, it will be done automatically"""
        assert isinstance(player, Player)
        if not self._tool_maker.can_make_action_on_tool_maker(player):
            return HasAction.NO_ACTION_POSSIBLE
        if self.make_action(player, [], []) == ActionResult.FAILURE:
            return HasAction.NO_ACTION_POSSIBLE
        return HasAction.AUTOMATIC_ACTION_DONE

    def new_turn(self) -> bool:
        """It is no way, that the tool maker location implies end of the game"""
        self._tool_maker.new_turn()
        return False
