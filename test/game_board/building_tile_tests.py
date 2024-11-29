import unittest
from typing import Iterable, Optional
from stone_age.game_board.building_tile import BuildingTile
from stone_age.game_board.simple_types import Player
from stone_age.game_board.arbitrary_building import ArbitraryBuilding
from stone_age.game_board.variable_building import VariableBuilding
from  stone_age.game_board.simple_building import SimpleBuilding
from stone_age.interfaces import InterfacePlayerBoardGameBoard
from stone_age.simple_types import HasAction, ActionResult, EndOfGameEffect
from stone_age.simple_types import PlayerOrder
from stone_age.simple_types import Effect

class MockInterfacePlayerBoardGameBoard(InterfacePlayerBoardGameBoard):

    def __init__(self) -> None:
        pass

    def give_effect(self, stuff: Iterable[Effect]) -> None:
        return None

    def give_end_of_the_game_effect(self, stuff: Iterable[EndOfGameEffect]) -> None:
        return None

    def give_figure(self) -> None:
        return None

    def take_resourses(self, stuff: Iterable[Effect]) -> bool:
        assert all(isinstance(effect, Effect) for effect in stuff)
        return True

    def take_figures(self, count: int) -> bool:
        assert isinstance(count, int)
        return True

    def has_figures(self, count: int) -> bool:
        assert isinstance(count, int)
        return True

    def has_sufficient_tools(self, goal: int) -> bool:
        assert isinstance(goal, int)
        return True

    def use_tool(self, idx: int) -> Optional[int]:
        return 1


class TestBuildingTile(unittest.TestCase):

    def __init__(self, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)
        self.building_tile: BuildingTile = BuildingTile(cards=[SimpleBuilding(
            [Effect.CLAY, Effect.GOLD, Effect.STONE])
            , ArbitraryBuilding(5), VariableBuilding(4, 2)])

    def set_up(self) -> None:
        pass

    def test_try_to_place_figures_success(self) -> None:
        player: Player = Player(PlayerOrder(0, 3), MockInterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        result: HasAction = self.building_tile.try_to_place_figures(player, count=1)
        self.assertEqual(result, HasAction.WAITING_FOR_PLAYER_ACTION)

    def test_try_to_place_figures_no_action_possible_too_many_figures(self) -> None:
        player: Player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        result: HasAction = self.building_tile.try_to_place_figures(player, count=2)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_place_figures_already_occupied(self) -> None:
        player: Player = Player(PlayerOrder(0, 2), MockInterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        self.building_tile.figures = player.player_order.forward()
        result: HasAction = self.building_tile.try_to_place_figures(player, count=1)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_place_figures_no_cards(self) -> None:
        self.building_tile = BuildingTile([])
        assert self.building_tile is not None
        player: Player = Player(PlayerOrder(2, 3), MockInterfacePlayerBoardGameBoard())
        result: HasAction = self.building_tile.try_to_place_figures(player, count=1)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_make_action_success(self) -> None:
        player: Player = Player(PlayerOrder(0, 2), MockInterfacePlayerBoardGameBoard())
        input_resources = [Effect.CLAY, Effect.GOLD, Effect.CLAY, Effect.GOLD]
        output_resources = []
        self.building_tile.place_figures(player, 1)
        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.ACTION_DONE)

    def test_place_figures_success(self) -> None:
        player: Player = Player(PlayerOrder(0, 4), MockInterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        result: bool = self.building_tile.place_figures(player, figure_count=1)
        self.assertTrue(result)
        self.assertEqual(self.building_tile.figures, player.player_order)


    def test_make_action_failure_due_to_figures_present(self) -> None:
        player = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        self.building_tile.figures = player.player_order.forward()
        input_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE]
        output_resources = []
        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.FAILURE)

    def test_make_action_failure_due_to_resource_mismatch(self) -> None:
        player = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        input_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE]
        output_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE, Effect.WOOD]
        assert self.building_tile is not None
        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.FAILURE)


    def test_skip_action_failure_no_figures(self) -> None:
        player = Player(PlayerOrder(2, 4), MockInterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        result = self.building_tile.skip_action(player)
        self.assertFalse(result)

    def test_skip_action_failure_too_much_figs(self) -> None:
        player = Player(PlayerOrder(2, 4), MockInterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        self.building_tile.place_figures(player, 2)
        result = self.building_tile.skip_action(player)
        self.assertFalse(result)

    def test_skip_action_failure_figure_mismatch(self) -> None:
        player = Player(PlayerOrder(3, 4), InterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        self.building_tile.figures = PlayerOrder(0, 4)
        result = self.building_tile.skip_action(player)
        self.assertFalse(result)

    def test_skip_action_success_remove_figure(self) -> None:
        player = Player(PlayerOrder(3, 4), MockInterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        self.building_tile.figures = player.player_order
        result = self.building_tile.skip_action(player)
        self.assertTrue(result)
        self.assertIsNone(self.building_tile.figures)

    # Tests for try_to_make_action
    def test_try_to_make_action_no_action_player_order_mismatch(self) -> None:
        player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        self.building_tile.figures = PlayerOrder(2, 4)
        result = self.building_tile.try_to_make_action(player)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_make_action_no_action_possible_no_cards(self) -> None:
        assert self.building_tile is not None
        self.building_tile.cards.clear()
        player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = player.player_order
        result = self.building_tile.try_to_make_action(player)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_make_action_no_action_possible_no_figures(self) -> None:
        assert self.building_tile is not None
        self.building_tile = BuildingTile(cards=[SimpleBuilding(
            [Effect.CLAY, Effect.GOLD, Effect.STONE])
            , ArbitraryBuilding(5), VariableBuilding(4, 2)])
        player = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = None
        result = self.building_tile.try_to_make_action(player)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_make_action_success(self) -> None:
        player = Player(PlayerOrder(0, 4), MockInterfacePlayerBoardGameBoard())
        assert self.building_tile is not None
        self.building_tile.place_figures(player, 1)
        result = self.building_tile.try_to_make_action(player)
        self.assertEqual(result, HasAction.WAITING_FOR_PLAYER_ACTION)


if __name__ == '__main__':
    unittest.main()
