import unittest
from unittest.mock import MagicMock
from stone_age.game_board.building_tile import BuildingTile
from stone_age.game_board.simple_types import Player
from stone_age.game_board.arbitrary_building import ArbitraryBuilding
from stone_age.game_board.variable_building import VariableBuilding
from  stone_age.game_board.simple_building import SimpleBuilding
from stone_age.interfaces import InterfacePlayerBoardGameBoard
from stone_age.simple_types import HasAction, ActionResult
from stone_age.simple_types import PlayerOrder
from stone_age.simple_types import Effect

class TestBuildingTile(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building_tile = None

    def set_up(self) -> None:
        self.building_tile = BuildingTile(cards=[SimpleBuilding(
            [Effect.CLAY,Effect.GOLD, Effect.STONE])
            , ArbitraryBuilding(5), VariableBuilding(4, 2)])

    def test_try_to_place_figures_success(self) -> None:
        player = Player(PlayerOrder(0, 3), InterfacePlayerBoardGameBoard())
        result = self.building_tile.try_to_place_figures(player, count=1)
        self.assertEqual(result, HasAction.AUTOMATIC_ACTION_DONE)

    def test_try_to_place_figures_no_action_possible_too_many_figures(self) -> None:
        player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        result = self.building_tile.try_to_place_figures(player, count=2)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_place_figures_already_occupied(self) -> None:
        player = Player(PlayerOrder(0, 2), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = player.player_order.forward()
        result = self.building_tile.try_to_place_figures(player, count=1)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_place_figures_no_cards(self) -> None:
        self.building_tile = BuildingTile([])
        player = Player(PlayerOrder(2, 3), InterfacePlayerBoardGameBoard())
        result = self.building_tile.try_to_place_figures(player, count=1)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_place_figures_success(self) -> None:
        self.set_up()
        player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        result = self.building_tile.place_figures(player, figure_count=1)
        self.assertTrue(result)
        self.assertEqual(self.building_tile.figures, player.player_order)


    def test_make_action_success(self) -> None:
        player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        input_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE]
        output_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE]
        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.ACTION_DONE)

    def test_make_action_failure_due_to_figures_present(self) -> None:
        player = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = player.player_order.forward()
        input_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE]
        output_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE]
        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.FAILURE)

    def test_make_action_failure_due_to_resource_mismatch(self) -> None:
        player = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        input_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE]
        output_resources = [Effect.CLAY, Effect.GOLD, Effect.STONE, Effect.WOOD]

        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.FAILURE)

    def test_make_action_failure_due_to_card_build_failure(self) -> None:
        player = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        input_resources = [Effect.CLAY, Effect.GOLD,
                           Effect.CLAY, Effect.GOLD, Effect.CLAY, Effect.GOLD]
        output_resources = [Effect.CLAY, Effect.GOLD,
                            Effect.CLAY, Effect.GOLD, Effect.CLAY, Effect.GOLD]
        self.building_tile.cards[-1].build = MagicMock(return_value=None)

        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.FAILURE)

    def test_make_action_failure_due_to_try_to_make_action(self) -> None:
        player = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        input_resources = [Effect(3)]
        output_resources = [Effect(3)]
        self.building_tile.try_to_make_action = MagicMock(
            return_value=HasAction.NO_ACTION_POSSIBLE)
        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.FAILURE)

    def test_make_action_failure_due_to_take_resources(self) -> None:
        player = Player(PlayerOrder(3, 4), InterfacePlayerBoardGameBoard())
        input_resources = [Effect(2)]
        output_resources = [Effect(2)]

        player.player_board.take_resources = MagicMock(return_value=False)

        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.FAILURE)

    def test_make_action_success_removes_card(self) -> None:
        player = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        input_resources = [Effect(5)]
        output_resources = [Effect(5)]

        # Ensure mock methods return valid success scenario
        self.building_tile.cards[-1].build = MagicMock(return_value=6)
        player.player_board.take_resources = MagicMock(return_value=True)

        result = self.building_tile.make_action(player, input_resources, output_resources)
        self.assertEqual(result, ActionResult.ACTION_DONE)
        self.assertEqual(len(self.building_tile.cards), 0)

    def test_skip_action_success_no_figures(self) -> None:
        player = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = None
        result = self.building_tile.skip_action(player)
        self.assertTrue(result)

    def test_skip_action_failure_figure_mismatch(self) -> None:
        player = Player(PlayerOrder(3, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = PlayerOrder(0, 4)
        result = self.building_tile.skip_action(player)
        self.assertFalse(result)

    def test_skip_action_success_remove_figure(self) -> None:
        player = Player(PlayerOrder(3, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = player.player_order  # Current player's figure
        result = self.building_tile.skip_action(player)
        self.assertTrue(result)
        self.assertIsNone(self.building_tile.figures)

    # Tests for try_to_make_action
    def test_try_to_make_action_no_action_player_order_mismatch(self) -> None:
        player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = PlayerOrder(2, 4) # Another player's figure
        result = self.building_tile.try_to_make_action(player)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_make_action_no_action_possible_no_cards(self) -> None:
        self.building_tile.cards.clear()  # No cards available
        player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = player.player_order
        result = self.building_tile.try_to_make_action(player)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_make_action_no_action_possible_no_figures(self) -> None:
        self.building_tile = BuildingTile(cards=[SimpleBuilding(
            [Effect.CLAY, Effect.GOLD, Effect.STONE])
            , ArbitraryBuilding(5), VariableBuilding(4, 2)])
        player = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = None  # No figure on the tile
        result = self.building_tile.try_to_make_action(player)
        self.assertEqual(result, HasAction.NO_ACTION_POSSIBLE)

    def test_try_to_make_action_success(self) -> None:
        player = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        self.building_tile.figures = player.player_order  # Current player's figure
        result = self.building_tile.try_to_make_action(player)
        self.assertEqual(result, HasAction.AUTOMATIC_ACTION_DONE)


if __name__ == '__main__':
    unittest.main()
