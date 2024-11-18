# pylint: disable=unused-argument, duplicate-code
from typing import Iterable, Optional, List
from stone_age.simple_types import Effect, HasAction, ActionResult
from stone_age.game_board.simple_types import Player


class Building:

    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        assert all(Effect.is_resource(x) for x in resources)


class InterfaceFigureLocationInternal:

    def place_figures(self, player: Player, figure_count: int) -> bool:
        assert isinstance(player, Player) and figure_count > 0

    def try_to_place_figures(self, player: Player, count: int) -> HasAction:
        assert isinstance(player, Player) and count > 0

    def make_action(self, player: Player, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert isinstance(player, Player)
        assert isinstance(input_resources, Iterable) and isinstance(output_resources, Iterable)

    def skip_action(self, player: Player) -> bool:
        assert isinstance(player, Player)

    def try_to_make_action(player: Player) -> HasAction:
        assert isinstance(player, Player)

    def new_turn(self) -> bool:
        pass
