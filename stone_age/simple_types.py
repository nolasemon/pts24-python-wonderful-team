from __future__ import annotations
from enum import IntEnum, Enum


class PlayerOrder:
    _order: int
    _players: int

    def __init__(self, order: int, players: int):
        self._order = order
        self._players = players

    @property
    def order(self) -> int:
        return self._order

    @property
    def players(self) -> int:
        return self._players

    def forward(self) -> PlayerOrder:
        forward: int = (self._order+1) % self._players
        return PlayerOrder(forward, self._players)

    def __str__(self) -> str:
        return str(self._order)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlayerOrder):
            return NotImplemented
        assert self._players == other.players
        return self._order == other.order


class Location(Enum):
    TOOL_MAKER = 1
    HUT = 2
    FIELD = 3
    HUNTING_GROUNDS = 4
    FOREST = 5
    CLAY_MOUND = 6
    QUARY = 7
    RIVER = 8
    CIVILISATION_CARD1 = 11
    CIVILISATION_CARD2 = 12
    CIVILISATION_CARD3 = 13
    CIVILISATION_CARD4 = 14
    BUILDING_TILE1 = 21
    BUILDING_TILE2 = 22
    BUILDING_TILE3 = 23
    BUILDING_TILE4 = 24


class Effect(IntEnum):
    FOOD = 1
    WOOD = 2
    CLAY = 3
    STONE = 4
    GOLD = 5
    TOOL = 6
    FIELD = 7
    BUILDING = 8
    ONE_TIME_TOOL2 = 12
    ONE_TIME_TOOL3 = 13
    ONE_TIME_TOOL4 = 14

    @staticmethod
    def is_resource(effect: Effect) -> bool:
        resources = (Effect.WOOD, Effect.CLAY, Effect.STONE, Effect.GOLD)
        return effect in resources

    @staticmethod
    def is_resource_or_food(effect: Effect) -> bool:
        return Effect.is_resource(effect) or effect == Effect.FOOD

    @staticmethod
    def points(effect: Effect) -> int:
        points_table = {
            Effect.FOOD: 2,
            Effect.WOOD: 3,
            Effect.CLAY: 4,
            Effect.STONE: 5,
            Effect.GOLD: 6,
        }
        return points_table.get(effect, 0)


class ActionResult(Enum):
    FAILURE = 1
    ACTION_DONE = 2
    ACTION_DONE_WAIT_FOR_TOOL_USE = 3
    ACTION_DONE_ALL_PLAYERS_TAKE_A_REWARD = 4


class HasAction(Enum):
    WAITING_FOR_PLAYER_ACTION = 1
    AUTOMATIC_ACTION_DONE = 2
    NO_ACTION_POSSIBLE = 3


class ImmediateEffect(Enum):
    THROW_WOOD = 1
    THROW_CLAY = 2
    THROW_STONE = 3
    THROW_GOLD = 4
    POINT = 5
    WOOD = 6
    CLAY = 7
    STONE = 8
    GOLD = 9
    CARD = 10
    ARBITRARY_RESOURCE = 11
    FOOD = 12


class EndOfGameEffect(IntEnum):
    FARMER = 1
    TOOL_MAKER = 2
    BUILDER = 3
    SHAMAN = 4
    MEDICINE = 5
    ART = 6
    MUSIC = 7
    WRITING = 8
    SUNDIAL = 9
    POTTERY = 10
    TRANSPORT = 11
    WEAVING = 12


class CivilisationCard:
    _immediate_effects: list[ImmediateEffect]
    _end_of_game_effects: list[EndOfGameEffect]

    def __init__(self, immediate_effects: list[ImmediateEffect],
                 end_of_game_effects: list[EndOfGameEffect]):
        self._immediate_effects = immediate_effects
        self._end_of_game_effects = end_of_game_effects

    @property
    def immediate_effects(self) -> list[ImmediateEffect]:
        return self._immediate_effects

    @property
    def end_of_game_effects(self) -> list[EndOfGameEffect]:
        return self._end_of_game_effects
