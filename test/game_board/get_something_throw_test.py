import unittest

from stone_age.simple_types import Effect
from stone_age.game_board.get_something_throw import GetSomethingThrow


class GetSomethingThrowTest(unittest.TestCase):
    def test_empty_resource(self) -> None:
        throw = GetSomethingThrow([])
        self.assertEqual(throw.resource, [])

    def test_single_resource(self) -> None:
        throw = GetSomethingThrow([Effect.WOOD])
        self.assertEqual(throw.resource, [Effect.WOOD])

    def test_multiple_resources(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY, Effect.STONE]
        throw = GetSomethingThrow(resources)
        self.assertEqual(throw.resource, resources)

    def test_duplicate_resources(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY, Effect.WOOD]
        throw = GetSomethingThrow(resources)
        self.assertEqual(throw.resource, resources)

    def test_state_empty(self) -> None:
        throw = GetSomethingThrow([])
        self.assertEqual(throw.state(), "Resources to get from throw: []")

    def test_state_single(self) -> None:
        throw = GetSomethingThrow([Effect.WOOD])
        self.assertEqual(
            throw.state(), "Resources to get from throw: [<Effect.WOOD: 2>]")

    def test_state_multiple(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY, Effect.STONE]
        throw = GetSomethingThrow(resources)
        self.assertEqual(throw.state(),
                         "Resources to get from throw: "
                         "[<Effect.WOOD: 2>, <Effect.CLAY: 3>, <Effect.STONE: 4>]")

    def test_state_duplicates(self) -> None:
        resources = [Effect.WOOD, Effect.CLAY, Effect.WOOD]
        throw = GetSomethingThrow(resources)
        self.assertEqual(throw.state(),
                         "Resources to get from throw: "
                         "[<Effect.WOOD: 2>, <Effect.CLAY: 3>, <Effect.WOOD: 2>]")
