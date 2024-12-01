from stone_age.player_board.player_board import PlayerBoard, PlayerBoardConfig
from stone_age.player_board.player_civilisation_cards import PlayerCivilisationCards
from stone_age.player_board.player_figures import PlayerFigures
from stone_age.player_board.player_resources_and_food import PlayerResourcesAndFood
from stone_age.player_board.player_tools import PlayerTools
from stone_age.player_board.tribe_fed_status import TribeFedStatus


def player_board_factory() -> PlayerBoard:
    civilisation_cards = PlayerCivilisationCards()
    figures = PlayerFigures()
    resources_and_food = PlayerResourcesAndFood()
    tools = PlayerTools()
    fed_status = TribeFedStatus(resources_and_food, figures)
    config = PlayerBoardConfig(
        0, 0,
        civilisation_cards,
        tools,
        resources_and_food,
        fed_status,
        figures,
    )
    player_board = PlayerBoard(config)
    return player_board
