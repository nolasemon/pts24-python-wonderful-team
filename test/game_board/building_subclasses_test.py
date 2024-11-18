import unittest
from stone_age.game_board.simple_building import SimpleBuilding
from stone_age.game_board.variable_building import VariableBuilding
from stone_age.game_board.arbitrary_building import ArbitraryBuilding
from stone_age.simple_types import Effect

class TestingBuildings(unittest.TestCase):

    def testing_simple_building(self) -> None:

        a = SimpleBuilding([Effect.CLAY, Effect.CLAY, Effect.CLAY, Effect.WOOD])
        self.assertListEqual(list(a.get_required_resources),
                             [Effect.CLAY, Effect.CLAY, Effect.CLAY, Effect.WOOD])
        self.assertIsNone(a.build((Effect.CLAY, Effect.CLAY, Effect.WOOD)))
        self.assertIsNone(a.build([]))
        self.assertEqual(a.build((Effect.CLAY, Effect.CLAY, Effect.CLAY, Effect.WOOD)), 15)
        self.assertIsNone(a.build((Effect.CLAY,Effect.CLAY, Effect.CLAY, Effect.GOLD)))
        self.assertIsNone(a.build([Effect.CLAY, Effect.CLAY, Effect.CLAY, Effect.WOOD,
                                   Effect.GOLD]))

        b = SimpleBuilding([])
        self.assertEqual(b.build(()), 0)
        self.assertIsNone(b.build([Effect.GOLD]))
        self.assertListEqual(list(b.get_required_resources), [])
        del b

        c = SimpleBuilding([Effect.WOOD, Effect.WOOD, Effect.WOOD])
        self.assertIsNone(c.build((Effect.WOOD, Effect.WOOD)))
        self.assertEqual(c.build((Effect.WOOD, Effect.WOOD, Effect.WOOD)), 9)
        self.assertIsNone(c.build((Effect.WOOD, Effect.WOOD, Effect.CLAY)))
        self.assertListEqual(list(c.get_required_resources),[Effect.WOOD, Effect.WOOD, Effect.WOOD])



    def testing_arbitraty_building(self) -> None:

        a = ArbitraryBuilding(6)
        self.assertEqual(a.get_max_number_of_resources, 6)
        self.assertIsNone(a.build(Effect.GOLD for x in range(7)))
        self.assertIsNone(a.build(set()))
        self.assertEqual(a.build([Effect.CLAY, Effect.CLAY,Effect.STONE, Effect.CLAY,
                                  Effect.WOOD, Effect.GOLD]), 26)
        self.assertNotEqual(a.build(Effect.WOOD for x in range(6)), 24)
        self.assertEqual(a.build([Effect.WOOD, Effect.WOOD, Effect.WOOD, Effect.WOOD,
                                  Effect.WOOD, Effect.WOOD]), 18)
        self.assertEqual(a.build([Effect.CLAY, Effect.STONE, Effect.GOLD, Effect.WOOD,
                                  Effect.WOOD]), 21)
        self.assertEqual(a.build([Effect.STONE, Effect.GOLD, Effect.WOOD, Effect.CLAY]),
                         18)

        with self.assertRaises(AssertionError):
            ArbitraryBuilding(-1)

        c = ArbitraryBuilding(4)
        self.assertEqual(c.build([Effect.GOLD, Effect.STONE, Effect.CLAY, Effect.WOOD]),
                         18)
        self.assertIsNone(c.build([Effect.GOLD, Effect.GOLD, Effect.GOLD, Effect.GOLD,
                                   Effect.GOLD]))
        self.assertEqual(c.get_max_number_of_resources, 4)
        c = ArbitraryBuilding(7)
        self.assertEqual(c.build([Effect.CLAY] * 7), 28)
        self.assertNotIn(c.build([Effect.GOLD] * 7), [x for x in range(35, 55) if x != 42])
        self.assertEqual(c.get_max_number_of_resources, 7)
        del c

    def testing_variable_building(self) -> None:

        a = VariableBuilding(6, 2)
        self.assertEqual(a.get_number_of_resources_types, 2)
        self.assertEqual(a.get_number_of_resources, 6)
        self.assertIsNone(a.build(Effect.GOLD for x in range(6)))
        self.assertIsNone(a.build([Effect.GOLD for x in range(6)] + [Effect.CLAY]))
        self.assertEqual(a.build([Effect.GOLD for x in range(5)] +
                                 [Effect.CLAY]), 34)
        self.assertIsNone(a.build([Effect.GOLD for x in range(5)] +
                                  [Effect.CLAY, Effect.STONE]))
        del a

        b = VariableBuilding(5, 3)
        self.assertEqual(b.get_number_of_resources_types, 3)
        self.assertEqual(b.get_number_of_resources, 5)
        with self.assertRaises(AssertionError):
            b = VariableBuilding(20, 0)
        with self.assertRaises(AssertionError):
            b = VariableBuilding(5, 5)
        c = VariableBuilding(3, 3)
        self.assertEqual(c.get_number_of_resources_types, 3)
        self.assertEqual(c.get_number_of_resources, 3)
        self.assertIsNone(c.build([Effect.CLAY, Effect.WOOD, Effect.GOLD, Effect.GOLD]))
        self.assertIsNone(c.build([Effect.CLAY, Effect.GOLD, Effect.GOLD]))
        self.assertEqual(c.build([Effect.WOOD, Effect.CLAY, Effect.STONE]), 12)
        del c, b

if __name__ == '__main__':
    unittest.main()
