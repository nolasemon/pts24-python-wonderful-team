import unittest
from stone_age.simple_types import Effect
from stone_age.player_board.player_resources_and_food import PlayerResourcesAndFood


class TestPlayerResourcesAndFood(unittest.TestCase):
    def setUp(self) -> None:
        self.resources = PlayerResourcesAndFood()

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
        self.resources.take_resources([Effect.WOOD])
        self.assertTrue(self.resources.has_resources([Effect.WOOD]))
        self.assertFalse(self.resources.has_resources(
            [Effect.WOOD, Effect.WOOD]))
        self.assertFalse(self.resources.has_resources([Effect.CLAY]))

    def test_has_resources_multiple(self) -> None:
        """Test checking for multiple resources."""
        resources_to_add = [Effect.WOOD, Effect.WOOD, Effect.CLAY]
        self.resources.take_resources(resources_to_add)

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

    def test_take_resources(self) -> None:
        """Test adding resources to inventory."""
        # Test taking single resource
        self.assertTrue(self.resources.take_resources([Effect.WOOD]))
        self.assertTrue(self.resources.has_resources([Effect.WOOD]))

        # Test taking multiple of same resource
        self.assertTrue(self.resources.take_resources(
            [Effect.WOOD, Effect.WOOD]))
        self.assertTrue(self.resources.has_resources(
            [Effect.WOOD, Effect.WOOD, Effect.WOOD]))

        # Test taking different resources
        self.assertTrue(self.resources.take_resources(
            [Effect.CLAY, Effect.STONE]))
        self.assertTrue(self.resources.has_resources([Effect.CLAY]))
        self.assertTrue(self.resources.has_resources([Effect.STONE]))

    def test_give_resources(self) -> None:
        """Test removing resources from inventory."""
        # Setup initial resources
        self.resources.take_resources([Effect.WOOD, Effect.WOOD, Effect.CLAY])

        # Test giving single resource
        self.assertTrue(self.resources.give_resources([Effect.WOOD]))
        self.assertTrue(self.resources.has_resources([Effect.WOOD]))
        self.assertFalse(self.resources.has_resources(
            [Effect.WOOD, Effect.WOOD]))

        # Test giving multiple resources
        self.assertTrue(self.resources.give_resources(
            [Effect.WOOD, Effect.CLAY]))
        self.assertFalse(self.resources.has_resources([Effect.WOOD]))
        self.assertFalse(self.resources.has_resources([Effect.CLAY]))

        # Test giving resources player doesn't have
        self.assertFalse(self.resources.give_resources([Effect.STONE]))
        self.assertFalse(self.resources.give_resources([Effect.WOOD]))

    def test_number_of_resources_for_final_points(self) -> None:
        """Test point calculation from resources."""
        # Test empty resources
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 0)

        # Test single resource
        self.resources.take_resources([Effect.WOOD])
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 3)

        # Test multiple resources
        self.resources.take_resources([
            Effect.CLAY,
            Effect.STONE,
            Effect.GOLD
        ])
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 18)

        # Test multiple of same resource
        self.resources.take_resources([Effect.GOLD])
        self.assertEqual(
            self.resources.number_of_resources_for_final_points(), 24)

    def test_state_representation(self) -> None:
        """Test string representation of resources."""
        # Test empty state
        state = self.resources.state()
        self.assertEqual(state, "")

        # Test with some resources
        self.resources.take_resources([Effect.WOOD, Effect.WOOD, Effect.CLAY])
        state = self.resources.state()
        state_lines = state.split('\n')
        self.assertEqual(len(state_lines), 2)
        self.assertIn('WOOD: 2', state)
        self.assertIn('CLAY: 1', state)

        # Test that resources with count 0 are not shown
        self.resources.give_resources([Effect.CLAY])
        state = self.resources.state()
        state_lines = state.split('\n')
        self.assertEqual(len(state_lines), 1)
        self.assertIn('WOOD: 2', state)
        self.assertNotIn('CLAY', state)

    def test_edge_cases(self) -> None:
        # Test giving more resources than available
        self.resources.take_resources([Effect.WOOD])
        self.assertFalse(self.resources.give_resources(
            [Effect.WOOD, Effect.WOOD]))

        # Test giving different resource than available
        self.assertFalse(self.resources.give_resources([Effect.CLAY]))

        # Test that resources can't go negative
        self.resources.give_resources([Effect.WOOD])
        self.assertFalse(self.resources.give_resources([Effect.WOOD]))

        # Test taking and giving large numbers of resources
        large_resource_list = [Effect.WOOD] * 1000
        self.resources.take_resources(large_resource_list)
        self.assertTrue(self.resources.has_resources(large_resource_list))
        self.assertTrue(self.resources.give_resources([Effect.WOOD] * 500))


if __name__ == '__main__':
    unittest.main()
