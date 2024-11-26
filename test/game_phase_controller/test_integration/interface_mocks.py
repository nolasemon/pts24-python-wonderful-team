from typing import Iterable, List

from stone_age.interfaces import InterfaceFeedTribe
from stone_age.interfaces import InterfaceToolUse
from stone_age.interfaces import InterfaceTakeReward
from stone_age.simple_types import Effect, HasAction, PlayerOrder


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
    try_responses: List[bool]

    def __init__(self) -> None:
        self.use_responses = []
        self.not_responses = []
        self.try_responses = []

    def use_tool(self, idx: int) -> bool:
        assert self.use_responses
        return self.use_responses.pop(0)

    def finish_using_tools(self) -> bool:
        assert self.not_responses
        return self.not_responses.pop(0)

    def can_use_tools(self) -> bool:
        assert self.try_responses
        return self.try_responses.pop(0)


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
