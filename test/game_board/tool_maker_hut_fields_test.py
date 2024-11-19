import unittest
from stone_age.simple_types import PlayerOrder
from stone_age.interfaces import InterfacePlayerBoardGameBoard
from stone_age.game_board.simple_types import Player
from stone_age.game_board.tool_maker_hut_fields import ToolMakerHutFields


class TestToolMakerHutFields(unittest.TestCase):

    def testing_less_then_2_players(self) -> None:
        with self.assertRaises(AssertionError):
            ToolMakerHutFields(0)
        with self.assertRaises(AssertionError):
            ToolMakerHutFields(1)

    def testing_2_players_both_tool_maker(self) -> None:
        t = ToolMakerHutFields(2)
        p1 = Player(PlayerOrder(0, 2), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 2), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_tool_maker(p1))
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.action_tool_maker(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_tool_maker(p2))
        self.assertFalse(t.place_on_tool_maker(p2))
        self.assertFalse(t.action_tool_maker(p2))
        self.assertEqual(len(t.tool_maker_figures), 1)
        self.assertEqual(t.tool_maker_figures[0], p1.player_order)
        del t
        del p1
        del p2

    def testing_2_players_both_hut(self) -> None:
        t = ToolMakerHutFields(2)
        p1 = Player(PlayerOrder(0, 2), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 2), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_hut(p1))
        self.assertTrue(t.place_on_hut(p1))
        self.assertTrue(t.action_hut(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_hut(p2))
        self.assertFalse(t.place_on_hut(p2))
        self.assertFalse(t.action_hut(p2))
        self.assertEqual(len(t.hut_figures), 2)
        self.assertEqual(t.hut_figures[0], p1.player_order)
        self.assertEqual(t.hut_figures[1], p1.player_order)
        del t
        del p1
        del p2

    def testing_2_players_both_fields(self) -> None:
        t = ToolMakerHutFields(2)
        p1 = Player(PlayerOrder(0, 2), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 2), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_fields(p1))
        self.assertTrue(t.place_on_fields(p1))
        self.assertTrue(t.action_fields(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_fields(p2))
        self.assertFalse(t.place_on_fields(p2))
        self.assertFalse(t.action_fields(p2))
        self.assertEqual(len(t.fields_figures), 1)
        self.assertEqual(t.fields_figures[0], p1.player_order)
        del t
        del p1
        del p2

    def testing_2_players_different_locations(self) -> None:
        t = ToolMakerHutFields(2)
        p1 = Player(PlayerOrder(0, 2), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 2), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_fields(p1))
        self.assertTrue(t.place_on_fields(p1))
        self.assertTrue(t.action_fields(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_hut(p2))
        self.assertTrue(t.place_on_hut(p2))
        self.assertTrue(t.action_hut(p2))
        self.assertFalse(t.can_place_at_all())
        self.assertEqual(len(t.fields_figures), 1)
        self.assertEqual(t.fields_figures[0], p1.player_order)
        self.assertEqual(len(t.hut_figures), 2)
        self.assertEqual(t.hut_figures[0], p2.player_order)
        self.assertEqual(t.hut_figures[1], p2.player_order)
        del t
        del p1
        del p2

    def testing_3_players_one_location(self) -> None:
        t = ToolMakerHutFields(3)
        p1 = Player(PlayerOrder(0, 3), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 3), InterfacePlayerBoardGameBoard())
        p3 = Player(PlayerOrder(2, 3), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_tool_maker(p1))
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.action_tool_maker(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_tool_maker(p2))
        self.assertFalse(t.place_on_tool_maker(p2))
        self.assertFalse(t.action_tool_maker(p2))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_tool_maker(p3))
        self.assertFalse(t.place_on_tool_maker(p3))
        self.assertFalse(t.action_tool_maker(p3))
        self.assertEqual(len(t.tool_maker_figures), 1)
        self.assertEqual(t.tool_maker_figures[0], p1.player_order)
        del t
        del p1
        del p2
        del p3

    def testing_3_players_two_locations(self) -> None:
        t = ToolMakerHutFields(3)
        p1 = Player(PlayerOrder(0, 3), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 3), InterfacePlayerBoardGameBoard())
        p3 = Player(PlayerOrder(2, 3), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_tool_maker(p1))
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.action_tool_maker(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_hut(p2))
        self.assertTrue(t.place_on_hut(p2))
        self.assertTrue(t.action_hut(p2))
        self.assertFalse(t.can_place_at_all())
        self.assertFalse(t.can_place_on_hut(p3))
        self.assertFalse(t.place_on_hut(p3))
        self.assertFalse(t.action_hut(p3))
        self.assertEqual(len(t.tool_maker_figures), 1)
        self.assertEqual(t.tool_maker_figures[0], p1.player_order)
        self.assertEqual(len(t.hut_figures), 2)
        self.assertEqual(t.hut_figures[0], p2.player_order)
        self.assertEqual(t.hut_figures[1], p2.player_order)
        del t
        del p1
        del p2
        del p3

    def testing_3_players_three_locations(self) -> None:
        t = ToolMakerHutFields(3)
        p1 = Player(PlayerOrder(0, 3), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 3), InterfacePlayerBoardGameBoard())
        p3 = Player(PlayerOrder(2, 3), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_tool_maker(p1))
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.action_tool_maker(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_hut(p2))
        self.assertTrue(t.place_on_hut(p2))
        self.assertTrue(t.action_hut(p2))
        self.assertFalse(t.can_place_at_all())
        self.assertFalse(t.can_place_on_fields(p3))
        self.assertFalse(t.place_on_fields(p3))
        self.assertFalse(t.action_fields(p3))
        self.assertEqual(len(t.tool_maker_figures), 1)
        self.assertEqual(t.tool_maker_figures[0], p1.player_order)
        self.assertEqual(len(t.hut_figures), 2)
        self.assertEqual(t.hut_figures[0], p2.player_order)
        self.assertEqual(t.hut_figures[1], p2.player_order)
        self.assertEqual(len(t.fields_figures), 0)
        del t
        del p1
        del p2
        del p3

    def testing_4_players_one_location(self) -> None:
        t = ToolMakerHutFields(4)
        p1 = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        p3 = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        p4 = Player(PlayerOrder(3, 4), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_tool_maker(p1))
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.action_tool_maker(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_tool_maker(p2))
        self.assertFalse(t.place_on_tool_maker(p2))
        self.assertFalse(t.action_tool_maker(p2))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_tool_maker(p3))
        self.assertFalse(t.place_on_tool_maker(p3))
        self.assertFalse(t.action_tool_maker(p3))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_tool_maker(p4))
        self.assertFalse(t.place_on_tool_maker(p4))
        self.assertFalse(t.action_tool_maker(p4))
        self.assertEqual(len(t.tool_maker_figures), 1)
        self.assertEqual(t.tool_maker_figures[0], p1.player_order)
        del t
        del p1
        del p2
        del p3
        del p4

    def testing_4_players_two_locations(self) -> None:
        t = ToolMakerHutFields(4)
        p1 = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        p3 = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        p4 = Player(PlayerOrder(3, 4), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_tool_maker(p1))
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.action_tool_maker(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_hut(p2))
        self.assertTrue(t.place_on_hut(p2))
        self.assertTrue(t.action_hut(p2))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_hut(p3))
        self.assertFalse(t.place_on_hut(p3))
        self.assertFalse(t.action_hut(p3))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_tool_maker(p4))
        self.assertFalse(t.place_on_tool_maker(p4))
        self.assertFalse(t.action_tool_maker(p4))
        self.assertEqual(len(t.tool_maker_figures), 1)
        self.assertEqual(t.tool_maker_figures[0], p1.player_order)
        self.assertEqual(len(t.hut_figures), 2)
        self.assertEqual(t.hut_figures[0], p2.player_order)
        self.assertEqual(t.hut_figures[1], p2.player_order)
        del t
        del p1
        del p2
        del p3
        del p4

    def testing_4_players_three_locations(self) -> None:
        t = ToolMakerHutFields(4)
        p1 = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        p3 = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        p4 = Player(PlayerOrder(3, 4), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_tool_maker(p1))
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.action_tool_maker(p1))
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_hut(p2))
        self.assertTrue(t.place_on_hut(p2))
        self.assertTrue(t.action_hut(p2))
        self.assertTrue(t.can_place_at_all())
        self.assertTrue(t.can_place_on_fields(p3))
        self.assertTrue(t.place_on_fields(p3))
        self.assertTrue(t.action_fields(p3))
        self.assertTrue(t.can_place_at_all())
        self.assertFalse(t.can_place_on_fields(p4))
        self.assertFalse(t.place_on_fields(p4))
        self.assertFalse(t.action_fields(p4))
        self.assertEqual(len(t.tool_maker_figures), 1)
        self.assertEqual(t.tool_maker_figures[0], p1.player_order)
        self.assertEqual(len(t.hut_figures), 2)
        self.assertEqual(t.hut_figures[0], p2.player_order)
        self.assertEqual(t.hut_figures[1], p2.player_order)
        self.assertEqual(len(t.fields_figures), 1)
        self.assertEqual(t.fields_figures[0], p3.player_order)
        del t
        del p1
        del p2
        del p3
        del p4

    def testing_player_places_at_same_location_twice(self) -> None:
        t = ToolMakerHutFields(4)
        p1 = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.place_on_fields(p1))
        self.assertFalse(t.can_place_on_fields(p1))
        self.assertFalse(t.place_on_fields(p1))
        del t
        del p1

    def testing_new_turn(self) -> None:
        t = ToolMakerHutFields(4)
        p1 = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        p3 = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.place_on_hut(p2))
        self.assertTrue(t.place_on_fields(p3))
        self.assertEqual(len(t.tool_maker_figures), 1)
        self.assertEqual(len(t.hut_figures), 2)
        self.assertEqual(len(t.fields_figures), 1)
        t.new_turn()
        self.assertEqual(len(t.tool_maker_figures), 0)
        self.assertEqual(len(t.hut_figures), 0)
        self.assertEqual(len(t.fields_figures), 0)
        self.assertTrue(t.can_place_on_tool_maker(p1))
        self.assertTrue(t.can_place_on_hut(p1))
        self.assertTrue(t.place_on_fields(p1))
        del t
        del p1
        del p2
        del p3

    def testing_state(self) -> None:
        t = ToolMakerHutFields(4)
        p1 = Player(PlayerOrder(0, 4), InterfacePlayerBoardGameBoard())
        p2 = Player(PlayerOrder(1, 4), InterfacePlayerBoardGameBoard())
        p3 = Player(PlayerOrder(2, 4), InterfacePlayerBoardGameBoard())
        p4 = Player(PlayerOrder(3, 4), InterfacePlayerBoardGameBoard())
        self.assertTrue(t.place_on_tool_maker(p1))
        self.assertTrue(t.place_on_hut(p2))
        self.assertTrue(t.place_on_fields(p3))
        self.assertFalse(t.place_on_fields(p4))
        self.assertEqual(t.state(), '{"tool maker figures": "0", "hut figures": "1", ' +
                         '"fields figures": "2", "restriction": 4}')


if __name__ == "__main__":
    unittest.main()
