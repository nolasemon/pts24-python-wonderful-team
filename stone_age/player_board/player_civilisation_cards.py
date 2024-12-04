from typing import Dict, List, Any, override
from collections import defaultdict
import json

from stone_age.interfaces import InterfaceGetState
from stone_age.simple_types import EndOfGameEffect


class PlayerCivilisationCards(InterfaceGetState):

    def __init__(self) -> None:
        self._end_effect_cards: Dict[EndOfGameEffect, int] = defaultdict(int)

    def add_end_of_game_effects(self, effects: List[EndOfGameEffect]) -> None:
        for effect in effects:
            self._end_effect_cards[effect] += 1

    def calculate_end_of_game_civilisation_card_points(
        self, buildings: int, tools: int, fields: int, figures: int
    ) -> int:
        result_points = 0

        for effect, count in self._end_effect_cards.items():
            match effect:
                case EndOfGameEffect.FARMER:
                    result_points += count * fields
                case EndOfGameEffect.TOOL_MAKER:
                    result_points += count * tools
                case EndOfGameEffect.BUILDER:
                    result_points += count * buildings
                case EndOfGameEffect.SHAMAN:
                    result_points += count * figures

        green_cards = [
            EndOfGameEffect.ART,
            EndOfGameEffect.MEDICINE,
            EndOfGameEffect.MUSIC,
            EndOfGameEffect.POTTERY,
            EndOfGameEffect.SUNDIAL,
            EndOfGameEffect.TRANSPORT,
            EndOfGameEffect.WEAVING,
            EndOfGameEffect.WRITING
        ]

        green_card_counts = [self._end_effect_cards[card]
                             for card in green_cards]

        while any(count > 0 for count in green_card_counts):
            set_size = sum(1 for count in green_card_counts if count > 0)
            result_points += set_size * set_size

            for i, count in enumerate(green_card_counts):
                if count > 0:
                    green_card_counts[i] -= 1

        return result_points

    @override
    def state(self) -> str:
        state: Any = {
            entry.name: self._end_effect_cards.get(entry, 0)
            for entry in EndOfGameEffect
        }
        return json.dumps(state)
