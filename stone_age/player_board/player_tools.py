from typing import List, Optional
from stone_age.interfaces import InterfaceGetState


class PlayerTools(InterfaceGetState):
    def __init__(self) -> None:
        self._tools: List[int] = []
        self._used_tools: List[bool] = []

    def new_turn(self) -> None:
        raise NotImplementedError

    def add_tool(self) -> None:
        raise NotImplementedError

    def add_single_use_tool(self, strength: int) -> None:
        raise NotImplementedError

    def use_tool(self, index: int) -> Optional[int]:
        raise NotImplementedError

    def has_sufficient_tools(self, goal: int) -> bool:
        raise NotImplementedError

    @property
    def tool_count(self) -> int:
        return len(self._tools)

    def state(self) -> str:
        raise NotImplementedError
