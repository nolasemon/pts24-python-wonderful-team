# pylint: disable=too-many-arguments, too-many-positional-arguments
from __future__ import annotations

from typing import Mapping, Iterable
import json

from stone_age.interfaces import InterfaceGetState, InterfaceStoneAgeGame, \
    InterfaceGamePhaseController
from stone_age.stone_age_observable import StoneAgeObservable
from stone_age.simple_types import PlayerOrder, Location, Effect


class StoneAgeGame(InterfaceStoneAgeGame):
    """This class has two primary responsibilities:

    1. converting integer `player_id` into `PlayerOrder` object and passing method
    calls to `InterfaceGamePhaseController` instance,
    2. updating game state (in `self._state`) and notifying observers via
    `StoneAgeObservable` class.
    """
    _players: Mapping[int, PlayerOrder]
    _state: str
    _player_boards: Mapping[PlayerOrder, InterfaceGetState]
    _game_board: InterfaceGetState
    _phase_controller: InterfaceGamePhaseController
    _observable: StoneAgeObservable

    def __init__(
        self,
        players: Mapping[int, PlayerOrder],
        player_boards: Mapping[PlayerOrder, InterfaceGetState],
        game_board: InterfaceGetState,
        phase_controller: InterfaceGamePhaseController,
        observable: StoneAgeObservable
    ) -> None:
        self._players = players
        self._player_boards = player_boards
        self._game_board = game_board
        self._phase_controller = phase_controller
        self._observable = observable
        self._update_state()

    def _update_state(self) -> None:
        """
        Method is responsible for collecting states from all components and
        saving it into `self._state`.
        """
        self._state = json.dumps({
            "player_board " + str(self._players[i]):
                json.loads(self._player_boards[self._players[i]].state())
            for i in sorted(self._players)
        } | {
            "game_board": json.loads(self._game_board.state()),
            "game_phase": json.loads(self._phase_controller.state())
        })

    def place_figures(self, player_id: int, location: Location, figures_count: int) -> bool:
        output: bool = self._phase_controller.place_figures(
            self._players[player_id],
            location,
            figures_count
        )
        self._update_state()
        self._observable.notify(self._state)
        return output

    def make_action(
        self,
        player_id: int,
        location: Location,
        used_resources: Iterable[Effect],
        desired_resource: Iterable[Effect]
    ) -> bool:
        output: bool = self._phase_controller.make_action(
            self._players[player_id],
            location,
            used_resources,
            desired_resource
        )
        self._update_state()
        self._observable.notify(self._state)
        return output

    def skip_action(self, player_id: int, location: Location) -> bool:
        output: bool = self._phase_controller.skip_action(
            self._players[player_id],
            location
        )
        self._update_state()
        self._observable.notify(self._state)
        return output

    def use_tools(self, player_id: int, tool_index: int) -> bool:
        output: bool = self._phase_controller.use_tools(
            self._players[player_id],
            tool_index
        )
        self._update_state()
        self._observable.notify(self._state)
        return output

    def no_more_tools_this_throw(self, player_id: int) -> bool:
        output: bool = self._phase_controller.no_more_tools_this_throw(
            self._players[player_id]
        )
        self._update_state()
        self._observable.notify(self._state)
        return output

    def feed_tribe(self, player_id: int, resources: Iterable[Effect]) -> bool:
        output: bool = self._phase_controller.feed_tribe(
            self._players[player_id],
            resources
        )
        self._update_state()
        self._observable.notify(self._state)
        return output

    def do_not_feed_this_turn(self, player_id: int) -> bool:
        output: bool = self._phase_controller.do_not_feed_this_turn(
            self._players[player_id]
        )
        self._update_state()
        self._observable.notify(self._state)
        return output

    def make_all_players_take_a_reward_choice(self, player_id: int, reward: Effect) -> bool:
        output: bool = self._phase_controller.make_all_players_take_a_reward_choice(
            self._players[player_id],
            reward
        )
        self._update_state()
        self._observable.notify(self._state)
        return output
