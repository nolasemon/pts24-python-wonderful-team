from typing import List, Dict, Optional, Any

from stone_age.game_board.interfaces import EvaluateCivilizationCardImmediateEffect
from stone_age.simple_types import PlayerOrder, Effect


class CivilizationCardPlace(EvaluateCivilizationCardImmediateEffect):
    def __init__(self, required_resources: int):
        self._required_resources = required_resources
        self._figures: List[PlayerOrder] = []
        self._available_cards: List[Dict[str, Any]] = []

    @property
    def required_resources(self) -> int:
        return self._required_resources

    @property
    def figures(self) -> List[PlayerOrder]:
        return self._figures

    @property
    def available_cards(self) -> List[Dict[str, Any]]:
        return self._available_cards

    def place_figure(self, player: PlayerOrder) -> bool:
        if self.figures:
            return False
        self._figures.append(player)
        return True

    def remove_figure(self, player: PlayerOrder) -> bool:
        try:
            self._figures.remove(player)
            return True
        except ValueError:
            return False

    def add_card(self, card: Dict[str, Any]) -> None:
        self._available_cards.append(card)

    def acquire_card(self, player: PlayerOrder, card_index: int) -> Optional[Dict[str, Any]]:
        if (self.figures and self.figures[0] == player
                and (0 <= card_index < len(self.available_cards))):
            acquired_card = self._available_cards.pop(card_index)
            self.remove_figure(player)
            return acquired_card

        return None

    def perform_effect(self, player: PlayerOrder, choice: Effect) -> bool:
        if not self.figures or self.figures[0] != player:
            return False

        print(f"Performing effect: {choice} for player {player}")
        return True

    def state(self) -> str:
        return (f"Civilization Card Place - Required Resources: {self.required_resources}, "
                f"Figures: {self.figures}, Cards: {self.available_cards}")
