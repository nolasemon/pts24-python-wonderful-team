from __future__ import annotations
from typing import Iterable

from stone_age.game_phase_controller.interfaces import GamePhaseStateFailureMeta
from stone_age.interfaces import InterfaceFeedTribe
from stone_age.simple_types import PlayerOrder, ActionResult, HasAction, Effect

class FeedTribeState(GamePhaseStateFailureMeta):
    _interface_feed_tribe: InterfaceFeedTribe

    def __init__(self, interface_feed_tribe: InterfaceFeedTribe):
        self._interface_feed_tribe = interface_feed_tribe

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        if self._interface_feed_tribe.feed_tribe(resources):
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def do_not_feed_this_turn(self, player: PlayerOrder) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        if self._interface_feed_tribe.do_not_feed_this_turn():
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        assert isinstance(player, PlayerOrder)
        if self._interface_feed_tribe.is_tribe_fed():
            return HasAction.NO_ACTION_POSSIBLE
        if self._interface_feed_tribe.feed_tribe_if_enough_food():
            return HasAction.AUTOMATIC_ACTION_DONE
        return HasAction.WAITING_FOR_PLAYER_ACTION
