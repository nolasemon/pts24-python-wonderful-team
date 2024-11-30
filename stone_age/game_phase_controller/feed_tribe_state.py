from __future__ import annotations
from typing import Iterable, Mapping

from stone_age.game_phase_controller.interfaces import GamePhaseStateFailureMeta
from stone_age.interfaces import InterfaceFeedTribe
from stone_age.simple_types import PlayerOrder, ActionResult, HasAction, Effect


class FeedTribeState(GamePhaseStateFailureMeta):
    _player_interfaces: Mapping[PlayerOrder, InterfaceFeedTribe]

    def __init__(self, player_interfaces: Mapping[PlayerOrder, InterfaceFeedTribe]):
        """Initializing with argument player_interfaces, 
        where each player has their own interface for feeding the tribe.
        When calling the particular methods, the right one is chosen."""
        self._player_interfaces = player_interfaces

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        if self._player_interfaces[player].feed_tribe(resources):
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def do_not_feed_this_turn(self, player: PlayerOrder) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        if self._player_interfaces[player].do_not_feed_this_turn():
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        assert isinstance(player, PlayerOrder)
        if self._player_interfaces[player].is_tribe_fed():
            return HasAction.NO_ACTION_POSSIBLE
        if self._player_interfaces[player].feed_tribe_if_enough_food():
            return HasAction.AUTOMATIC_ACTION_DONE
        return HasAction.WAITING_FOR_PLAYER_ACTION
