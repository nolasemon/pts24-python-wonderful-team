from typing import Optional, Union, Iterable
import json
from stone_age.game_board.simple_types import Player
from stone_age.simple_types import PlayerOrder
from stone_age.game_board.interfaces import InterfaceFigureLocationInternal
from stone_age.game_board import simple_building
from stone_age.game_board import variable_building
from stone_age.game_board import arbitrary_building
from stone_age.simple_types import HasAction, Effect, ActionResult


class BuildingTile(InterfaceFigureLocationInternal):

    def __init__(self, cards: Iterable[Union[simple_building.SimpleBuilding,
        arbitrary_building.ArbitraryBuilding,
        variable_building.VariableBuilding]]):
        self.cards: list[Union[simple_building.SimpleBuilding,
        arbitrary_building.ArbitraryBuilding,
        variable_building.VariableBuilding]] = list(cards)
        self.figures: Optional[PlayerOrder] = None


    def place_figures(self, player: Player, figure_count: int) -> bool:
        if self.try_to_place_figures(player, figure_count) != HasAction.NO_ACTION_POSSIBLE:
            player.player_board.take_figures(1)
            self.figures = player.player_order
            return True
        return False


    def try_to_place_figures(self, player: Player, count: int) -> HasAction:
        assert isinstance(player, Player) and count > 0
        if count > 1:
            return HasAction.NO_ACTION_POSSIBLE
        if not player.player_board.has_figures(count):
            return HasAction.NO_ACTION_POSSIBLE
        if self.figures is not None:
            return HasAction.NO_ACTION_POSSIBLE
        if not self.cards:
            return HasAction.NO_ACTION_POSSIBLE
        return HasAction.WAITING_FOR_PLAYER_ACTION

    def make_action(self, player: Player, input_resources: Iterable[Effect],
                    output_resources: Iterable[Effect]) -> ActionResult:
        if self.figures is None:
            return ActionResult.FAILURE
        card: Union[simple_building.SimpleBuilding,
        arbitrary_building.ArbitraryBuilding,
        variable_building.VariableBuilding] = self.cards[-1]
        result: Optional[int] = card.build(input_resources)
        if (result is None or
                self.try_to_make_action(player) == HasAction.NO_ACTION_POSSIBLE):
            return ActionResult.FAILURE
        if player.player_board.take_resourses(input_resources):
            self.figures = None
            self.cards.pop()
            return ActionResult.ACTION_DONE
        return ActionResult.FAILURE

    def skip_action(self, player: Player) -> bool:
        if self.figures is not None and player.player_order != self.figures:
            return False
        if self.figures is None:
            return False
        player.player_board.give_figure()
        self.figures = None
        return True

    def try_to_make_action(self, player: Player) -> HasAction:
        assert isinstance(player, Player)
        if player.player_order != self.figures:
            return HasAction.NO_ACTION_POSSIBLE
        if not self.cards:
            return HasAction.NO_ACTION_POSSIBLE
        if not self.figures:
            return HasAction.NO_ACTION_POSSIBLE
        return HasAction.WAITING_FOR_PLAYER_ACTION

    def new_turn(self) -> bool:
        if not self.cards:
            return True
        return False

    def state(self) -> str:
        d: dict[str, str] = {"TakenBy": f"{self.figures}"
        if self.figures is not None else "None",
                             "CardsInPile": "[]" if not self.cards else
                             "\n".join(x.state() for x in self.cards)}
        return json.dumps(d)
