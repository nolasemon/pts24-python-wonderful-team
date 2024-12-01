# pylint: disable=unused-argument, duplicate-code
from typing import Iterable, Optional
from stone_age.game_board.simple_types import Player
from stone_age.simple_types import Effect, HasAction, ActionResult


class Building:

    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        assert False


class InterfaceFigureLocationInternal:

    def place_figures(self, player: Player, figure_count: int) -> bool:
        assert False

    def try_to_place_figures(self, player: Player, count: int) -> HasAction:
        assert False

    def make_action(self, player: Player, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert False

    def skip_action(self, player: Player) -> bool:
        assert False

    def try_to_make_action(self, player: Player) -> HasAction:
        assert False

    def new_turn(self) -> bool:
        assert False


class EvaluateCivilizationCardImmediateEffect:
    def perform_effect(self, player: Player, choice: Iterable[Effect]) -> ActionResult:
        assert False


class InterfaceCurrentThrow:
    def initiate(self, player: Player, choice: Effect, dices: int) -> None:
        assert False
