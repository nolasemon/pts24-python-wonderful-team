# pylint: disable=unused-argument, duplicate-code
from __future__ import annotations
from typing import Iterable
from stone_age.simple_types import PlayerOrder, Location, Effect


class InterfaceGamePhaseController:
    def place_figures(self, player: PlayerOrder, location: Location, figures_count: int) -> bool:
        assert False

    def make_action(self, player: PlayerOrder, location: Location,
                    input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> bool:
        assert False

    def skip_action(self, player: PlayerOrder, location: Location) -> bool:
        assert False

    def use_tools(self, player: PlayerOrder, tool_index: int) -> bool:
        assert False

    def no_more_tools_this_throw(self, player: PlayerOrder) -> bool:
        assert False

    def feed_tribe(self, player: PlayerOrder, resources: Iterable[Effect]) -> bool:
        assert False

    def do_not_feed_this_turn(self, player: PlayerOrder) -> bool:
        assert False

    def make_all_players_take_a_reward_choice(self, player: PlayerOrder, reward: Effect) -> bool:
        assert False

    def state(self) -> str:
        assert False


class InterfaceGetState:
    def get_state(self) -> str:
        assert False
