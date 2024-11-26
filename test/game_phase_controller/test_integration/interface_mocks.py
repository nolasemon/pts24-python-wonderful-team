from __future__ import annotations
from typing import List, Iterable

from stone_age.interfaces import InterfaceFigureLocation, InterfaceNewTurn, \
    InterfaceFeedTribe, InterfaceToolUse, InterfaceTakeReward
from stone_age.simple_types import HasAction, ActionResult, PlayerOrder, Effect


class LocationMock(InterfaceFigureLocation):
    place_responses: List[bool]
    try_place_responses: List[HasAction]
    make_action_responses: List[ActionResult]
    skip_action_responses: List[bool]
    try_make_responses: List[HasAction]
    new_turn_responses: List[bool]

    def __init__(self):
        self.place_responses = []
        self.try_place_responses = []
        self.make_action_responses = []
        self.skip_action_responses = []
        self.try_make_responses = []
        self.new_turn_responses = []

    def place_figures(self, player: PlayerOrder, figure_count: int) -> bool:
        assert self.place_responses
        return self.place_responses.pop(0)

    def try_to_place_figures(self, player: PlayerOrder, count: int) -> HasAction:
        assert self.try_place_responses
        return self.try_place_responses.pop(0)

    def make_action(self, player: PlayerOrder, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert self.make_action_responses
        return self.make_action_responses.pop(0)

    def skip_action(self, player: PlayerOrder) -> bool:
        assert self.skip_action_responses
        return self.skip_action_responses.pop(0)

    def try_to_make_action(self, player: PlayerOrder) -> HasAction:
        assert self.try_make_responses
        return self.try_make_responses.pop(0)

    def new_turn(self) -> bool:
        assert self.new_turn_responses
        return self.new_turn_responses.pop(0)


class NewTurnMock(InterfaceNewTurn):
    def new_turn(self) -> None:
        pass


class FeedMock(InterfaceFeedTribe):
    pass


class ToolUseMock(InterfaceToolUse):
    pass


class RewardMock(InterfaceTakeReward):
    pass