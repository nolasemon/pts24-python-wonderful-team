class PlayerFigures:

    def __init__(self) -> None:
        self._total_figures: int = 0
        self._figures: int = 0

    def add_new_figure(self) -> bool:
        if 0 <= self.get_total_figures < 10:
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
        return f"Actual figures count: {self._figures},\nTotal figures: {self.get_total_figures}"
