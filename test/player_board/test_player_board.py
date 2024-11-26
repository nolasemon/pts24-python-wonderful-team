import unittest
from unittest.mock import Mock
from stone_age.player_board.player_board import PlayerBoard, PlayerBoardConfig
from stone_age.player_board.player_civilisation_cards import PlayerCivilisationCards
from stone_age.player_board.player_tools import PlayerTools
from stone_age.player_board.player_resources_and_food import PlayerResourcesAndFood
from stone_age.player_board.tribe_fed_status import TribeFedStatus
from stone_age.player_board.player_figures import PlayerFigures


class TestPlayerBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.cards = Mock(spec=PlayerCivilisationCards)
        self.tools = Mock(spec=PlayerTools)
        self.resources_and_food = Mock(spec=PlayerResourcesAndFood)
        self.fed_status = Mock(spec=TribeFedStatus)
        self.figures = Mock(spec=PlayerFigures)

        # Set up default mock return values
        self.cards.state.return_value = "Mock cards state"
        self.tools.state.return_value = "Mock tools state"
        self.resources_and_food.state.return_value = "Mock resources state"
        self.fed_status.state.return_value = "Mock fed status state"
        self.figures.state.return_value = "Mock figures state"

        config = PlayerBoardConfig(
            points=0,
            houses=0,
            cards=self.cards,
            tools=self.tools,
            resources_and_food=self.resources_and_food,
            fed_status=self.fed_status,
            figures=self.figures
        )
        self.board = PlayerBoard(config)

    def test_initial_state(self) -> None:
        """Test initial state of the player board"""
        state = self.board.state()
        self.assertIn('"points": 0', state)
        self.assertIn('"houses": 0', state)
        self.assertIn("Mock cards state", state)
        self.assertIn("Mock tools state", state)
        self.assertIn("Mock resources state", state)
        self.assertIn("Mock fed status state", state)
        self.assertIn("Mock figures state", state)

    def test_add_points(self) -> None:
        """Test adding points"""
        self.board.add_points(5)
        self.assertIn('"points": 5', self.board.state())
        self.board.add_points(3)
        self.assertIn('"points": 8', self.board.state())

    def test_add_house(self) -> None:
        """Test adding houses"""
        self.board.add_house()
        self.assertIn('"houses": 1', self.board.state())
        self.board.add_house()
        self.assertIn('"houses": 2', self.board.state())

    def test_add_end_of_game_points(self) -> None:
        """Test end of game points calculation"""
        self.resources_and_food.number_of_resources_for_final_points.return_value = 10
        self.cards.calculate_end_of_game_civilisation_card_points.return_value = 15
        self.tools.tool_count.return_value = 3
        self.fed_status.fields.return_value = 4
        self.figures.get_total_figures.return_value = 5

        self.board.add_points(5)

        self.board.add_end_of_game_points()

        # Verify final points (5 initial + 10 resources + 15 civilization cards = 30)
        self.assertIn('"points": 30', self.board.state())

    def test_add_end_of_game_points_with_houses(self) -> None:
        """Test end of game points calculation with houses"""
        self.resources_and_food.number_of_resources_for_final_points.return_value = 5
        self.cards.calculate_end_of_game_civilisation_card_points.return_value = 10

        # Add houses and initial points
        self.board.add_house()
        self.board.add_house()
        self.board.add_points(3)

        self.board.add_end_of_game_points()

        # Verify final points (3 initial + 5 resources + 10 civilization cards = 18)
        self.assertIn('"points": 18', self.board.state())
