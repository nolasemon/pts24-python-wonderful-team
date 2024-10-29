from enum import Enum


class GamePhase(Enum):
    PLACE_FIGURES = 1
    MAKE_ACTION = 2
    FEED_TRIBE = 3
    NEW_ROUND = 4
    WAITING_FOR_TOOL_USE = 5
    ALL_PLAYERS_TAKE_A_REWARD = 6
    GAME_END = 7
