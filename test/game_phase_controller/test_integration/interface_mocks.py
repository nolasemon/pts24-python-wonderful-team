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

    def __init__(self) -> None:
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


class FeedTribeMock(InterfaceFeedTribe):
    enough_responses: List[bool]
    feed_responses: List[bool]
    not_feed_responses: List[bool]
    is_fed_responses: List[bool]

    def __init__(self) -> None:
        self.enough_responses = []
        self.feed_responses = []
        self.not_feed_responses = []
        self.is_fed_responses = []

    def feed_tribe_if_enough_food(self) -> bool:
        assert self.enough_responses
        return self.enough_responses.pop(0)

    def feed_tribe(self, resources: Iterable[Effect]) -> bool:
        assert self.feed_responses
        return self.feed_responses.pop(0)

    def do_not_feed_this_turn(self) -> bool:
        assert self.not_feed_responses
        return self.not_feed_responses.pop(0)

    def is_tribe_fed(self) -> bool:
        assert self.is_fed_responses
        return self.is_fed_responses.pop(0)


class ToolUseMock(InterfaceToolUse):
    use_responses: List[bool]
    not_responses: List[bool]
    can_responses: List[bool]

    def __init__(self) -> None:
        self.use_responses = []
        self.not_responses = []
        self.can_responses = []

    def use_tool(self, idx: int) -> bool:
        assert self.use_responses
        return self.use_responses.pop(0)

    def finish_using_tools(self) -> bool:
        assert self.not_responses
        return self.not_responses.pop(0)

    def can_use_tools(self) -> bool:
        assert self.can_responses
        return self.can_responses.pop(0)


class RewardMock(InterfaceTakeReward):
    take_responses: List[bool]
    auto_responses: List[HasAction]

    def __init__(self) -> None:
        self.take_responses = []
        self.auto_responses = []

    def take_reward(self, player: PlayerOrder, reward: Effect) -> bool:
        assert self.take_responses
        return self.take_responses.pop(0)

    def try_make_action(self, player: PlayerOrder) -> HasAction:
        assert self.auto_responses
        return self.auto_responses.pop(0)
