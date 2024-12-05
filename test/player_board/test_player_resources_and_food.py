import unittest
import json
from typing import Any

from stone_age.simple_types import Effect
from stone_age.player_board.player_resources_and_food import PlayerResourcesAndFood


class TestPlayerResourcesAndFood(unittest.TestCase):
    def setUp(self) -> None:
        self.resources = PlayerResourcesAndFood()

    def test_state_isolated(self) -> None:
        self.resources._resources = {  # pylint: disable=protected-access
            Effect.WOOD: 42,
            Effect.CLAY: 255,
            Effect.FOOD: -2,
            Effect.GOLD: 0,
        }
        s: Any = json.loads(self.resources.state())
        self.assertEqual(s, {"WOOD": 42, "CLAY": 255,
                         "FOOD": -2, "GOLD": 0, "STONE": 0})

    def test_state_representation(self) -> None:
        """Test string representation of resources."""
        # Test empty state
        s1: Any = json.loads(self.resources.state())
        self.assertEqual(
            s1, {key: 0 for key in ["WOOD", "STONE", "CLAY", "GOLD", "FOOD"]})

        # Test with some resources
        self.resources.give_resources([Effect.WOOD, Effect.WOOD, Effect.CLAY])
        s2: str = self.resources.state()
        self.assertIn('"WOOD": 2', s2)
        self.assertIn('"CLAY": 1', s2)

        # Test that resources with count 0 are not shown
        self.resources.take_resources([Effect.CLAY])
        s3: str = self.resources.state()
        self.assertIn('"WOOD": 2', s3)
        self.assertIn('"CLAY": 0', s3)

    def test_initial_state(self) -> None:
        """Test that all resources start at zero."""
        for effect in Effect:
            self.assertTrue(self.resources.has_resources([effect] * 0))
            self.assertFalse(self.resources.has_resources([effect]))

    def test_has_resources_empty_list(self) -> None:
        """Test that empty resource list always returns True."""
        self.assertTrue(self.resources.has_resources([]))

    def test_has_resources_single(self) -> None:
        """Test checking for a single resource."""
        self.resources.give_resources([Effect.WOOD])
        self.assertTrue(self.resources.has_resources([Effect.WOOD]))
        self.assertFalse(self.resources.has_resources(
            [Effect.WOOD, Effect.WOOD]))
        self.assertFalse(self.resources.has_resources([Effect.CLAY]))

    def test_has_resources_multiple(self) -> None:
        """Test checking for multiple resources."""
        resources_to_add = [Effect.WOOD, Effect.WOOD, Effect.CLAY]
        self.resources.give_resources(resources_to_add)

        # Test exact amount
        self.assertTrue(self.resources.has_resources(
            [Effect.WOOD, Effect.WOOD]))
        self.assertTrue(self.resources.has_resources([Effect.CLAY]))

        # Test insufficient amount
        self.assertFalse(self.resources.has_resources(
            [Effect.WOOD, Effect.WOOD, Effect.WOOD]))

        # Test mixed resources
        self.assertTrue(self.resources.has_resources(
            [Effect.WOOD, Effect.CLAY]))
        self.assertFalse(self.resources.has_resources(
            [Effect.WOOD, Effect.STONE]))

    def test_give_resources(self) -> None:
        """Test adding resources to inventory."""
        # Test taking single resource
        self.assertTrue(self.resources.give_resources([Effect.WOOD]))
        self.assertTrue(self.resources.has_resources([Effect.WOOD]))

        # Test taking multiple of same resource
        self.assertTrue(self.resources.give_resources(
            [Effect.WOOD, Effect.WOOD]))
        self.assertTrue(self.resources.has_resources(
            [Effect.WOOD, Effect.WOOD, Effect.WOOD]))

        # Test taking different resources
        self.assertTrue(self.resources.give_resources(
            [Effect.CLAY, Effect.STONE]))
        self.assertTrue(self.resources.has_resources([Effect.CLAY]))
        self.assertTrue(self.resources.has_resources([Effect.STONE]))

    def test_take_resources(self) -> None:
        """Test removing resources from inventory."""
        # Setup initial resources
        self.resources.give_resources([Effect.WOOD, Effect.WOOD, Effect.CLAY])

        # Test giving single resource
        self.assertTrue(self.resources.take_resources([Effect.WOOD]))
        self.assertTrue(self.resources.has_resources([Effect.WOOD]))
        self.assertFalse(self.resources.has_resources(
            [Effect.WOOD, Effect.WOOD]))

        # Test giving multiple resources
        self.assertTrue(self.resources.take_resources(
            [Effect.WOOD, Effect.CLAY]))
        self.assertFalse(self.resources.has_resources([Effect.WOOD]))
        self.assertFalse(self.resources.has_resources([Effect.CLAY]))

        # Test giving resources player doesn't have
        self.assertFalse(self.resources.take_resources([Effect.STONE]))
        self.assertFalse(self.resources.take_resources([Effect.WOOD]))

    def test_number_of_resources_for_final_points(self) -> None:
        """Test point calculation from resources."""
        # Test empty resources
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 0)

        # Test single resource
        self.resources.give_resources([Effect.WOOD])
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 1)

        # Test food
        self.resources.give_resources([Effect.FOOD])
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 1)

        # Test multiple resources
        self.resources.give_resources([
            Effect.CLAY,
            Effect.STONE,
            Effect.GOLD
        ])
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 4)

        # Test multiple of same resource
        self.resources.give_resources([Effect.GOLD])
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 5)

        self.resources.give_resources([Effect.FOOD])
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 5)

    def test_edge_cases(self) -> None:
        # Test giving more resources than available
        self.resources.give_resources([Effect.WOOD])
        self.assertFalse(self.resources.take_resources(
            [Effect.WOOD, Effect.WOOD]))

        # Test giving different resource than available
        self.assertFalse(self.resources.take_resources([Effect.CLAY]))

        # Test that resources can't go negative
        self.resources.take_resources([Effect.WOOD])
        self.assertFalse(self.resources.take_resources([Effect.WOOD]))

        # Test taking and giving large numbers of resources
        large_resource_list = [Effect.WOOD] * 1000
        self.resources.give_resources(large_resource_list)
        self.assertTrue(self.resources.has_resources(large_resource_list))
        self.assertTrue(self.resources.take_resources([Effect.WOOD] * 500))


if __name__ == '__main__':
    unittest.main()
