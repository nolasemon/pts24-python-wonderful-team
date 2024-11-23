from __future__ import annotations

from stone_age.game_phase_controller.interfaces import GamePhaseStateFailureMeta
from stone_age.interfaces import InterfaceToolUse
from stone_age.simple_types import PlayerOrder, ActionResult, HasAction


class WaitingForToolUseState(GamePhaseStateFailureMeta):
    _interface_tool_use: InterfaceToolUse

    def __init__(self, interface_tool_use: InterfaceToolUse):
        self._interface_tool_use = interface_tool_use

    def use_tools(self, player: PlayerOrder, tool_index: int) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        assert isinstance(tool_index, int)
        if self._interface_tool_use.use_tool(tool_index):
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE
    
    def no_more_tools_this_throw(self, player: PlayerOrder) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        if self._interface_tool_use.finish_using_tools():
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        assert isinstance(player, PlayerOrder)
        if not self._interface_tool_use.can_use_tools():
            return HasAction.NO_ACTION_POSSIBLE
        return HasAction.WAITING_FOR_PLAYER_ACTION