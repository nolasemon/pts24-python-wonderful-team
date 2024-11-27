import json
from typing import Any


class PlayerFigures:

    def __init__(self, figures_start: int = 5, figures_maximum: int = 10) -> None:
        assert 0 <= figures_start <= figures_maximum and figures_maximum > 0

        self._figures_maximum = figures_maximum
        self._total_figures: int = figures_start
        self._figures: int = figures_start

    def add_new_figure(self) -> bool:
        if 0 <= self.get_total_figures < self._figures_maximum:
            self._total_figures += 1
            self._figures += 1
            return True
        return False

    def has_figures(self, count: int) -> bool:
        return self._figures >= count

    @property
    def get_total_figures(self) -> int:
        return self._total_figures

    def take_figures(self, count: int) -> bool:
        if count > 0 and self.has_figures(count):
            self._figures -= count
            return True
        return False

    def new_turn(self) -> None:
        if self._figures == 0:
            self._figures = self.get_total_figures

    def state(self) -> str:
        state: Any = {
            "figures on player board": self._figures,
            "total figures": self._total_figures,
        }
        return json.dumps(state)
