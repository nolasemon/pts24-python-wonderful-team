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
        """With 2 and 3 players, only 2 of these locations may be occupied during a round:
           tool maker, hut, and field"""
        if self.restriction == 4:
            return True
        is_tool_maker_occupied: bool = not self.tool_maker_figures
        is_hut_occupied: bool = not self.hut_figures
        is_fields_occupied: bool = not self.fields_figures
        return (int(is_tool_maker_occupied) + int(is_hut_occupied) + int(is_fields_occupied)) < 2

    def place_on_tool_maker(self, player: Player) -> bool:
        if not self.can_place_on_tool_maker(player):
            return False
        self.tool_maker_figures.append(player.player_order)
        return True

    def action_tool_maker(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if len(self.tool_maker_figures) == 0:
            return False
        if self.tool_maker_figures[0] != player.player_order:
            return False
        player.player_board.give_effect([Effect.TOOL])
        return True

    def can_place_on_tool_maker(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if not self.can_place_at_all():
            return False
        if len(self.tool_maker_figures) > 0:
            return False
        return True

    def place_on_hut(self, player: Player) -> bool:
        if not self.can_place_on_tool_maker(player):
            return False
        self.hut_figures.append(player.player_order)
        self.hut_figures.append(player.player_order)
        return True

    def action_hut(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if len(self.hut_figures) == 0:
            return False
        if self.hut_figures[0] != player.player_order:
            return False
        player.player_board.give_figure()
        return True

    def can_place_on_hut(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if not self.can_place_at_all():
            return False
        if len(self.hut_figures) > 0:
            return False
        return True

    def place_on_fields(self, player: Player) -> bool:
        if not self.can_place_on_fields(player):
            return False
        self.fields_figures.append(player.player_order)
        return True

    def action_fields(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if len(self.fields_figures) == 0:
            return False
        if self.fields_figures[0] != player.player_order:
            return False
        player.player_board.give_effect([Effect.FIELD])
        return True

    def can_place_on_fields(self, player: Player) -> bool:
        assert isinstance(player, Player)
        if not self.can_place_at_all():
            return False
        if len(self.fields_figures) > 0:
            return False
        return True

    def new_turn(self) -> None:
        """When all actions are done, figures are taken back on player boards,
           so locations must be clear"""
        self.tool_maker_figures.clear()
        self.hut_figures.clear()
        self.fields_figures.clear()

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
