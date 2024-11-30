import json
from typing import List, Any
from stone_age.game_board.simple_types import Player
from stone_age.simple_types import PlayerOrder, Effect


class ToolMakerHutFields:
    _tool_maker_figures: List[PlayerOrder]
    _hut_figures: List[PlayerOrder]
    _fields_figures: List[PlayerOrder]
    _restriction: int

    def __init__(self, player_count: int):
        assert isinstance(player_count, int) and 2 <= player_count <= 4
        self._tool_maker_figures: List[PlayerOrder] = []
        self._hut_figures: List[PlayerOrder] = []
        self._fields_figures: List[PlayerOrder] = []
        self._restriction = player_count

    @property
    def tool_maker_figures(self) -> List[PlayerOrder]:
        return self._tool_maker_figures

    @property
    def hut_figures(self) -> List[PlayerOrder]:
        return self._hut_figures

    @property
    def fields_figures(self) -> List[PlayerOrder]:
        return self._fields_figures

    @property
    def restriction(self) -> int:
        return self._restriction

    def can_place_at_all(self) -> bool:
        """
        Always returns true when there isn't player restriction (there are 4 players)
        With 2 and 3 players, only 2 of these locations may be occupied during a round:
        tool maker, hut, and field
        """
        if self.restriction == 4:
            return True
        is_tool_maker_occupied: bool = len(self.tool_maker_figures) > 0
        is_hut_occupied: bool = len(self.hut_figures) > 0
        is_fields_occupied: bool = len(self.fields_figures) > 0
        return (int(is_tool_maker_occupied) + int(is_hut_occupied) + int(is_fields_occupied)) < 2

    def place_on_tool_maker(self, player: Player) -> bool:
        if not self.can_place_on_tool_maker(player):
            return False
        player.player_board.take_figures(1)
        self.tool_maker_figures.append(player.player_order)
        return True

    def action_tool_maker(self, player: Player) -> bool:
        """The tool maker location will be clear after performing the action"""
        if not self.can_make_action_on_tool_maker(player):
            return False
        player.player_board.give_effect([Effect.TOOL])
        player.player_board.give_figure()
        self.tool_maker_figures.clear()
        return True

    def can_place_on_tool_maker(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if not player.player_board.has_figures(1):
            return False
        if not self.can_place_at_all():
            return False
        if len(self.tool_maker_figures) > 0:
            return False
        return True

    def can_make_action_on_tool_maker(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if len(self.tool_maker_figures) == 0:
            return False
        if self.tool_maker_figures[0] != player.player_order:
            return False
        return True

    def place_on_hut(self, player: Player) -> bool:
        if not self.can_place_on_hut(player):
            return False
        player.player_board.take_figures(2)
        self.hut_figures.append(player.player_order)
        self.hut_figures.append(player.player_order)
        return True

    def action_hut(self, player: Player) -> bool:
        """The hut location will be clear after performing the action"""
        if not self.can_make_action_on_hut(player):
            return False
        player.player_board.give_figure()
        player.player_board.give_figure()
        player.player_board.give_figure()
        self.hut_figures.clear()
        return True

    def can_place_on_hut(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if not player.player_board.has_figures(2):
            return False
        if not self.can_place_at_all():
            return False
        if len(self.hut_figures) > 0:
            return False
        return True

    def can_make_action_on_hut(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if len(self.hut_figures) == 0:
            return False
        if self.hut_figures[0] != player.player_order:
            return False
        return True

    def place_on_fields(self, player: Player) -> bool:
        if not self.can_place_on_fields(player):
            return False
        player.player_board.take_figures(1)
        self.fields_figures.append(player.player_order)
        return True

    def action_fields(self, player: Player) -> bool:
        """Fields location will be clear after performing the action"""
        if not self.can_make_action_on_fields(player):
            return False
        player.player_board.give_effect([Effect.FIELD])
        player.player_board.give_figure()
        self.fields_figures.clear()
        return True

    def can_place_on_fields(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if not player.player_board.has_figures(1):
            return False
        if not self.can_place_at_all():
            return False
        if len(self.fields_figures) > 0:
            return False
        return True

    def can_make_action_on_fields(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if len(self.fields_figures) == 0:
            return False
        if self.fields_figures[0] != player.player_order:
            return False
        return True

    def new_turn(self) -> bool:
        """
        THIS IS NOT THE SAME new_turn() LIKE IN InterfaceFigureLocationInternal
        Returns true if locations are clear and prepared for the new turn
        """
        return len(self.tool_maker_figures) == 0 and len(self.hut_figures) == 0 and\
            len(self.fields_figures) == 0

    def state(self) -> str:
        state: Any = {
            "tool maker figures": "None" if len(self.tool_maker_figures) == 0
            else str(self.tool_maker_figures[0]),
            "hut figures": "None" if len(self.hut_figures) == 0
            else str(self.hut_figures[0]),
            "fields figures": "None" if len(self.fields_figures) == 0
            else str(self._fields_figures[0]),
            "restriction": self.restriction
        }
        return json.dumps(state)
