from __future__ import annotations
from typing import Iterable, Mapping

from stone_age.game_phase_controller.interfaces import GamePhaseStateFailureMeta
from stone_age.interfaces import InterfaceFeedTribe
from stone_age.simple_types import PlayerOrder, ActionResult, HasAction, Effect

class FeedTribeState(GamePhaseStateFailureMeta):
    _dict_player_interface: Mapping[PlayerOrder, InterfaceFeedTribe]

    def __init__(self, dict_player_interface: Mapping[PlayerOrder, InterfaceFeedTribe]):
        """Initializing with argument dict_player_interface, 
        where each player has their own interface for feeding the tribe.
        When calling the particular methods, the right one is chosen."""
        self._dict_player_interface = dict(dict_player_interface)

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        if self._dict_player_interface[player].feed_tribe(resources):
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def do_not_feed_this_turn(self, player: PlayerOrder) -> ActionResult:
        assert isinstance(player, PlayerOrder)
        if self._dict_player_interface[player].do_not_feed_this_turn():
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def try_to_make_automatic_action(self, player: PlayerOrder) -> HasAction:
        assert isinstance(player, PlayerOrder)
        if self._dict_player_interface[player].is_tribe_fed():
            return HasAction.NO_ACTION_POSSIBLE
        if self._dict_player_interface[player].feed_tribe_if_enough_food():
            return HasAction.AUTOMATIC_ACTION_DONE
        return HasAction.WAITING_FOR_PLAYER_ACTION
