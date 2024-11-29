# pylint: disable=unused-argument, duplicate-code
from typing import Iterable, Optional, List
from stone_age.game_board.simple_types import Player
from stone_age.simple_types import Effect, HasAction, ActionResult, PlayerOrder


class Building:

    def build(self, resources: Iterable[Effect]) -> Optional[int]:
        assert all(Effect.is_resource(x) for x in resources)
        return sum(Effect.points(x) for x in resources)


class InterfaceFigureLocationInternal:

    def place_figures(self, player: Player, figure_count: int) -> bool:
        assert isinstance(player, Player) and figure_count > 0
        return False

    def try_to_place_figures(self, player: Player, count: int) -> HasAction:
        assert isinstance(player, Player) and count > 0
        return HasAction.NO_ACTION_POSSIBLE

    def make_action(self, player: Player, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        assert isinstance(player, Player)
        assert isinstance(input_resources, Iterable) and isinstance(
            output_resources, Iterable)
        return ActionResult.FAILURE

    def skip_action(self, player: Player) -> bool:
        assert isinstance(player, Player)
        return False

    def try_to_make_action(self, player: Player) -> HasAction:
        assert isinstance(player, Player)
        return HasAction.NO_ACTION_POSSIBLE

    def new_turn(self) -> bool:
        return False


class EvaluateCivilizationCardImmediateEffect:
    def perform_effect(self, player: Player, choice: Iterable[Effect]) -> ActionResult:
        assert False


class InterfaceCurrentThrow:
    def initiate(self, player: Player, choice: Effect, dices: int) -> None:
        assert False


class InterfaceRewardMenu:
    def initiate(self, rewards: Iterable[Effect]) -> None:
        assert False

    def take_reward(self, player: PlayerOrder, reward: Effect) -> bool:
        assert False

    def try_make_action(self, player: PlayerOrder) -> HasAction:
        assert False


class InterfaceThrow:
    def throw(self, num_dice: int) -> List[int]:
        assert False
