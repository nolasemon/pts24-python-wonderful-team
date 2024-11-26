from typing import List, Optional
from stone_age.interfaces import InterfaceGetState


class PlayerTools(InterfaceGetState):

    def __init__(self) -> None:
        self._tools: List[int] = [0] * 3
        self._used_tools: List[bool] = [False] * 3

    def new_turn(self) -> None:
        self._used_tools = [False for _ in range(len(self._tools))]

    def add_tool(self) -> None:
        minimal_tool: int = min(self._tools)
        minimal_tool_index: int = self._tools.index(minimal_tool)

        if minimal_tool < 4 and minimal_tool_index < 3:
            self._tools[minimal_tool_index] += 1

    def add_single_use_tool(self, strength: int) -> None:
        if 2 <= strength <= 4:
            self._tools.append(strength)
            self._used_tools.append(False)

    def use_tool(self, index: int) -> Optional[int]:
        if index < 0 or index >= len(self._tools):
            return None

        element: int = self._tools[index]
        if self._used_tools[index] or element == 0:
            return None

        if index < 3:
            self._used_tools[index] = True
        else:
            del self._used_tools[index], self._tools[index]

        return element

    def has_sufficient_tools(self, goal: int) -> bool:
        strength_sum: int = 0

        for index, tool in enumerate(self._tools):
            if not self._used_tools[index]:
                strength_sum += tool

        return strength_sum >= goal
      
    @property
    def tool_count(self) -> int:
        return len(self._tools)

    def state(self) -> str:
        return '\n'.join([f"{'Single-use tool: ' if index >= 3 else f'Tool {index + 1}: '}"
                          f"{strength}, {'used' if self._used_tools[index] else 'unused'}"
                          for index, strength in enumerate(self._tools) if strength != 0])
