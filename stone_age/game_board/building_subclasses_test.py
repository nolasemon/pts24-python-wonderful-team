from simple_building import SimpleBuilding
from variable_building import VariableBuilding
from arbitrary_building import ArbitraryBuilding
from unittest import TestCase
from stone_age.simple_types import Effect

class Testing_Buildings(TestCase):

    def testing_SimpleBuilding(self) -> None:

        a = SimpleBuilding([Effect.CLAY, Effect.CLAY, Effect.CLAY, Effect.WOOD])
        self.assertListEqual(a.get_required_resources,[Effect.CLAY, Effect.CLAY, Effect.CLAY, Effect.WOOD])
        self.assertIsNone(a.build((Effect.CLAY, Effect.CLAY, Effect.WOOD)))
        self.assertIsNone(a.build([]))
        self.assertIsNone(a.build([x for x in range(0, 5, -1)] + [Effect.CLAY]))
        self.assertEqual(a.build((Effect.CLAY, Effect.CLAY, Effect.CLAY, Effect.WOOD)), 15)
        self.assertIsNone(a.build((Effect.CLAY, Effect.CLAY, Effect.CLAY, Effect.GOLD)))

        with self.assertRaises(TypeError):
            a.build(None)
        with self.assertRaises(TypeError):
            a.build(999)
        with self.assertRaises(TypeError):
            a.build(Effect.CLAY)
        del a

        b = SimpleBuilding([])
        self.assertEqual(b.build(()), 0)
        self.assertIsNone(a.build([Effect.GOLD]))
        del b

        c = SimpleBuilding([Effect.WOOD, Effect.WOOD, Effect.WOOD])
        self.assertIsNone(c.build((Effect.WOOD, Effect.WOOD)))
        self.assertEqual(c.build((Effect.WOOD, Effect.WOOD, Effect.WOOD)), 10)
        self.assertIsNone(c.build((Effect.WOOD, Effect.WOOD, Effect.CLAY)))

        with self.assertRaises(TypeError):
            c.build(lambda z: z ** 0.5)
        with self.assertRaises(TypeError):
            c.build("Effect.WOOD")
        with self.assertRaises(AssertionError):
            c.build("Effect.WOOD Effect.WOOD Effect.WOOD".split(' '))
        with self.assertRaises(TypeError):
            c.build(bool(0))
        del c


    def testing_ArbitratyBuilding(self) -> None:

        a = ArbitraryBuilding(6)
        self.assertEqual(a.get_maxNumberOfResources, 6)
        self.assertIsNone(a.build(Effect.GOLD for x in range(7)))
        self.assertIsNone(a.build(set()))
        self.assertEqual(a.build([Effect.CLAY, Effect.CLAY,Effect.STONE, Effect.CLAY, Effect.WOOD, Effect.GOLD]), 26)
        self.assertIsNone(a.build({x for x in (["Clay"] * 6)}))
        self.assertNotEqual(a.build(Effect.WOOD for x in range(6)), 24)
        self.assertEqual(a.build([Effect.WOOD, Effect.WOOD, Effect.WOOD, Effect.WOOD, Effect.WOOD, Effect.WOOD]), 18)
        self.assertEqual(a.build([Effect.CLAY, Effect.STONE, Effect.GOLD, Effect.WOOD, Effect.WOOD]), 27)
        self.assertEqual(a.build([Effect.STONE, Effect.GOLD, Effect.WOOD, Effect.CLAY]), 18)

        with self.assertRaises(TypeError):
            a.build(None)
        with self.assertRaises(TypeError):
            a.build(777)
        with self.assertRaises(TypeError):
            a.build(Effect.WOOD)
        with self.assertRaises(TypeError):
            a.build("Effect.WOOD")
        with self.assertRaises(AssertionError):
            a.build("Effect.STONE Effect.GOLD Effect.WOOD".split(' '))
        with self.assertRaises(TypeError):
            a.build(5 > 7)
        with self.assertRaises(TypeError):
            a.build(lambda x, y: 3 * y - x ** 2)
        del a


        with self.assertRaises(AssertionError):
            b = ArbitraryBuilding(-1)
        del b

        c = ArbitraryBuilding(4)
        self.assertEqual(c.build([Effect.GOLD, Effect.STONE, Effect.CLAY, Effect.WOOD]), 18)
        self.assertIsNone(c.build([Effect.GOLD, Effect.GOLD, Effect.GOLD, Effect.GOLD, Effect.GOLD]))
        c = ArbitraryBuilding(7)
        self.assertEqual(c.build([Effect.CLAY] * 7), 28)
        self.assertNotIn(c.build([Effect.GOLD] * 7), [x for x in range(35, 55) if x != 42])
        del c

