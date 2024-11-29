import unittest
from typing import Iterable

from stone_age.game_phase_controller.waiting_for_tool_use_state import WaitingForToolUseState
from stone_age.interfaces import InterfaceToolUse
from stone_age.simple_types import PlayerOrder, ActionResult, HasAction, Location, Effect


class ToolUseMock(InterfaceToolUse):
    _use_response: bool
    _not_response: bool
    _try_response: bool

    def __init__(self, use_response: bool = False, not_response: bool = False,
                 try_response: bool = False):
        self._use_response = use_response
        self._not_response = not_response
        self._try_response = try_response

    def use_tool(self, idx: int) -> bool:
        return self._use_response

    def finish_using_tools(self) -> bool:
        return self._not_response

    def can_use_tools(self) -> bool:
        return self._try_response


class TestWaitingForToolUseState(unittest.TestCase):
    def test_use_tool_method(self) -> None:
        player = PlayerOrder(1, 1)
        idx: int = 1
        tool_use_failure = ToolUseMock()
        wait_for_tool_use_failure = WaitingForToolUseState(tool_use_failure)
        self.assertEqual(ActionResult.FAILURE,
                         wait_for_tool_use_failure.use_tools(player, idx))
        tool_use_done = ToolUseMock(use_response=True)
        wait_for_tool_use_done = WaitingForToolUseState(tool_use_done)
        self.assertEqual(ActionResult.ACTION_DONE,
                         wait_for_tool_use_done.use_tools(player, idx))

    def test_no_more_tools_this_throw_method(self) -> None:
        player = PlayerOrder(1, 1)
        tool_use_failure = ToolUseMock()
        wait_for_tool_use_failure = WaitingForToolUseState(tool_use_failure)
        self.assertEqual(ActionResult.FAILURE,
                         wait_for_tool_use_failure.no_more_tools_this_throw(player))
        tool_use_done = ToolUseMock(not_response=True)
        wait_for_tool_use_done = WaitingForToolUseState(tool_use_done)
        self.assertEqual(ActionResult.ACTION_DONE,
                         wait_for_tool_use_done.no_more_tools_this_throw(player))

    def try_to_make_automatic_action_method(self) -> None:
        player = PlayerOrder(1, 1)
        tool_use_failure = ToolUseMock()
        wait_for_tool_use_failure = WaitingForToolUseState(tool_use_failure)
        self.assertEqual(HasAction.NO_ACTION_POSSIBLE,
                         wait_for_tool_use_failure.try_to_make_automatic_action(player))
        tool_use_wait = ToolUseMock(try_response=True)
        wait_for_tool_use = WaitingForToolUseState(tool_use_wait)
        self.assertEqual(HasAction.WAITING_FOR_PLAYER_ACTION,
                         wait_for_tool_use.try_to_make_automatic_action(player))

    def test_wrong_action_this_phase(self) -> None:
        mock = ToolUseMock()
        waiting_for_tool_use_state = WaitingForToolUseState(mock)
        player = PlayerOrder(1, 1)
        place = Location.FIELD
        in_resources: Iterable[Effect] = []
        out_resources: Iterable[Effect] = []
        self.assertEqual(ActionResult.FAILURE,
                         waiting_for_tool_use_state.make_action(player, place,
                                                                in_resources,
                                                                out_resources))
