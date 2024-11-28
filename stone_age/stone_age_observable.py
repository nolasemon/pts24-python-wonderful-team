from __future__ import annotations

from typing import Dict

from stone_age.interfaces import InterfaceStoneAgeObservable, InterfaceStoneAgeObserver


class StoneAgeObservable(InterfaceStoneAgeObservable):
    _observers: Dict[int, InterfaceStoneAgeObserver]

    def __init__(self) -> None:
        self._observers = {}

    def register_observer(self, player_id: int, observer: InterfaceStoneAgeObserver) -> None:
        self._observers[player_id] = observer

    def notify(self, game_state: str) -> None:
        for observer in self._observers.values():
            observer.update(game_state)
