import unittest
import json
from typing import Any

from stone_age.simple_types import Effect
from stone_age.player_board.player_figures import PlayerFigures
from stone_age.player_board.player_resources_and_food import PlayerResourcesAndFood
from stone_age.player_board.tribe_fed_status import TribeFedStatus


class TestTribeFedStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.resources_and_food = PlayerResourcesAndFood()
        self.figures = PlayerFigures(figures_start=10)
        self.fed_status = TribeFedStatus(self.resources_and_food, self.figures)

    def test_state(self) -> None:
        s1: Any = json.loads(self.fed_status.state())
        self.assertEqual(s1, {"tribe fed": False, "fields": 0})

        self.fed_status._fields = 1337  # pylint: disable=protected-access
        self.fed_status._tribe_fed = True  # pylint: disable=protected-access
        s2: Any = json.loads(self.fed_status.state())
        self.assertEqual(s2, {"tribe fed": True, "fields": 1337})

    def test_no_food(self) -> None:
        self.assertFalse(self.fed_status.feed_tribe_if_enough_food())
        self.assertFalse(self.fed_status.feed_tribe([]))
        self.assertTrue(self.fed_status.set_tribe_fed())
        s: Any = json.loads(self.fed_status.state())
        self.assertEqual(s, {"tribe fed": True, "fields": 0})

    def test_add_field(self) -> None:
        self.fed_status.add_field()
        s1: Any = json.loads(self.fed_status.state())
        self.assertEqual(s1, {"tribe fed": False, "fields": 1})

        self.fed_status.add_field()
        self.fed_status.add_field()
        s2: Any = json.loads(self.fed_status.state())
        self.assertEqual(s2, {"tribe fed": False, "fields": 3})

        for _ in range(100):
            self.fed_status.add_field()
        s3: Any = json.loads(self.fed_status.state())
        self.assertEqual(
            s3, {"tribe fed": False, "fields": TribeFedStatus.MAX_FIELDS})

    def test_feed_if_enough_food_success(self) -> None:
        self.resources_and_food.give_resources([Effect.FOOD] * 10)
        self.assertTrue(self.fed_status.feed_tribe_if_enough_food())
        s: Any = json.loads(self.fed_status.state())
        self.assertEqual(s, {"tribe fed": True, "fields": 0})
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))

    def test_feed_tribe_with_resources(self) -> None:
        self.resources_and_food.give_resources([Effect.FOOD] * 8)
        self.assertFalse(self.fed_status.feed_tribe_if_enough_food())
        self.assertFalse(self.fed_status.feed_tribe(
            [Effect.WOOD, Effect.CLAY]))
        self.resources_and_food.give_resources([Effect.WOOD, Effect.CLAY])
        self.assertTrue(self.fed_status.feed_tribe([Effect.WOOD, Effect.CLAY]))
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))
        s: Any = json.loads(self.fed_status.state())
        self.assertEqual(s, {"tribe fed": True, "fields": 0})

    def test_feed_tribe_unsuccessful(self) -> None:
        self.resources_and_food.give_resources([Effect.FOOD] * 8)
        self.assertFalse(self.fed_status.feed_tribe_if_enough_food())
        self.assertFalse(self.fed_status.feed_tribe([]))
        self.assertTrue(self.fed_status.set_tribe_fed())
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))
        s1: Any = json.loads(self.fed_status.state())
        self.assertEqual(s1, {"tribe fed": True, "fields": 0})

        self.fed_status.new_turn()

        self.resources_and_food.give_resources(
            [Effect.FOOD] * 7 + [Effect.CLAY, Effect.GOLD])
        self.assertFalse(self.fed_status.feed_tribe_if_enough_food())
        self.assertFalse(self.fed_status.feed_tribe(
            [Effect.CLAY, Effect.GOLD]))
        self.assertTrue(self.fed_status.set_tribe_fed())
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))
        s2: Any = json.loads(self.fed_status.state())
        self.assertEqual(s2, {"tribe fed": True, "fields": 0})

    def test_multiple_calls_food(self) -> None:
        self.resources_and_food.give_resources([Effect.FOOD] * 5)
        self.assertFalse(self.fed_status.feed_tribe_if_enough_food())
        self.assertFalse(self.fed_status.feed_tribe([]))
        s1: Any = json.loads(self.fed_status.state())
        self.assertEqual(s1, {"tribe fed": False, "fields": 0})
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))

        self.resources_and_food.give_resources([Effect.FOOD] * 5)
        self.assertTrue(self.fed_status.feed_tribe_if_enough_food())
        s2: Any = json.loads(self.fed_status.state())
        self.assertEqual(s2, {"tribe fed": True, "fields": 0})
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))

    def test_feed_with_fields(self) -> None:
        self.resources_and_food.give_resources([Effect.FOOD] * 8)
        self.fed_status.add_field()
        self.fed_status.add_field()
        self.assertTrue(self.fed_status.feed_tribe_if_enough_food())
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))
        s: Any = json.loads(self.fed_status.state())
        self.assertEqual(s, {"tribe fed": True, "fields": 2})

    def test_new_turn(self) -> None:
        self.resources_and_food.give_resources([Effect.FOOD] * 8)
        self.fed_status.add_field()
        self.fed_status.add_field()
        self.fed_status.feed_tribe_if_enough_food()

        self.fed_status.new_turn()
        s1: Any = json.loads(self.fed_status.state())
        self.assertEqual(s1, {"tribe fed": False, "fields": 2})

        for _ in range(8):
            self.fed_status.add_field()

        self.assertTrue(self.fed_status.feed_tribe_if_enough_food())
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))
        s: Any = json.loads(self.fed_status.state())
        self.assertEqual(s, {"tribe fed": True, "fields": 10})

    def test_surplus_food(self) -> None:
        for _ in range(5):
            self.fed_status.add_field()
        self.resources_and_food.give_resources(
            [Effect.FOOD] * 11 + [Effect.CLAY] * 5)
        self.assertTrue(self.fed_status.feed_tribe_if_enough_food())
        s: Any = json.loads(self.fed_status.state())
        self.assertEqual(s, {"tribe fed": True, "fields": 5})
        self.assertTrue(
            self.resources_and_food.has_resources([Effect.FOOD] * 6))
        self.assertFalse(
            self.resources_and_food.has_resources([Effect.FOOD] * 7))
        self.assertTrue(
            self.resources_and_food.has_resources([Effect.CLAY] * 5))
        self.assertFalse(
            self.resources_and_food.has_resources([Effect.CLAY] * 6))

    def test_surplus_resources(self) -> None:
        for _ in range(5):
            self.fed_status.add_field()

        self.resources_and_food.give_resources([Effect.GOLD] * 6)
        self.assertFalse(self.fed_status.feed_tribe_if_enough_food())
        self.assertTrue(self.fed_status.feed_tribe([Effect.GOLD] * 5))
        s: Any = json.loads(self.fed_status.state())
        self.assertEqual(s, {"tribe fed": True, "fields": 5})
        self.assertTrue(self.resources_and_food.has_resources([Effect.GOLD]))
        self.assertFalse(
            self.resources_and_food.has_resources([Effect.GOLD] * 2))

    def test_surplus_both(self) -> None:
        for _ in range(5):
            self.fed_status.add_field()

        self.resources_and_food.give_resources(
            [Effect.FOOD] * 4 + [Effect.CLAY] * 3)
        self.assertFalse(self.fed_status.feed_tribe_if_enough_food())
        self.assertTrue(self.fed_status.feed_tribe([Effect.CLAY]))
        s: Any = json.loads(self.fed_status.state())
        self.assertEqual(s, {"tribe fed": True, "fields": 5})
        self.assertFalse(self.resources_and_food.has_resources([Effect.FOOD]))
        self.assertTrue(
            self.resources_and_food.has_resources([Effect.CLAY] * 2))
        self.assertFalse(
            self.resources_and_food.has_resources([Effect.CLAY] * 3))
