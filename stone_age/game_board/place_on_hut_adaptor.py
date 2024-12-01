# pylint: disable=duplicate-code
from typing import Iterable
from stone_age.simple_types import HasAction, Effect, ActionResult
from stone_age.game_board.simple_types import Player
from stone_age.game_board.interfaces import InterfaceFigureLocationInternal
from stone_age.game_board.tool_maker_hut_fields import ToolMakerHutFields


class PlaceOnHutAdaptor(InterfaceFigureLocationInternal):
    _hut: ToolMakerHutFields

    def __init__(self, hut: ToolMakerHutFields):
        assert isinstance(hut, ToolMakerHutFields)
        self._hut: ToolMakerHutFields = hut

    def place_figures(self, player: Player, figure_count: int) -> bool:
        assert isinstance(player, Player) and figure_count > 0
        if self.try_to_place_figures(player, figure_count) == HasAction.NO_ACTION_POSSIBLE:
            return False
        self._hut.place_on_hut(player)
        return True

    def try_to_place_figures(self, player: Player, count: int) -> HasAction:
        """
        If a figure can be placed, we wait for a player, otherwise there is
        no action possible.
        """
        assert isinstance(player, Player) and count > 0
        if count != 2:
            return HasAction.NO_ACTION_POSSIBLE
        if not self._hut.can_place_on_hut(player):
            return HasAction.NO_ACTION_POSSIBLE
        return HasAction.WAITING_FOR_PLAYER_ACTION

    def make_action(self, player: Player, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        """
        The player needs neither input nor output resources to make an action on the hut.
        After the action location must be clear and prepared for a new turn.
        """
        assert isinstance(player, Player)
        assert all(isinstance(effect, Effect) for effect in input_resources)
        assert all(isinstance(effect, Effect) for effect in output_resources)
        if input_resources:
            return ActionResult.FAILURE
        if output_resources:
            return ActionResult.FAILURE
        if not self._hut.action_hut(player):
            return ActionResult.FAILURE
        self._hut.new_turn()
        return ActionResult.ACTION_DONE

    def skip_action(self, player: Player) -> bool:
        """It is no way, that player can take her figure and leave the hut in place"""
        return False

    def try_to_make_action(self, player: Player) -> HasAction:
        """If action can be made, it will be done automatically"""
        assert isinstance(player, Player)
        if not self._hut.can_make_action_on_hut(player):
            return HasAction.NO_ACTION_POSSIBLE
        if self.make_action(player, [], []) == ActionResult.FAILURE:
            return HasAction.NO_ACTION_POSSIBLE
        return HasAction.AUTOMATIC_ACTION_DONE

    def new_turn(self) -> bool:
        """It is no way, that the hut location implies end of the game"""
        self._hut.new_turn()
        return False
