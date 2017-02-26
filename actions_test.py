from action import *
from player import Player
from house import Room
from field import Field
from constants import *
import unittest


def init_player():
    return Player('foo')


class ActionsTest(unittest.TestCase):

    def test_occupation_action(self):
        player = init_player()
        args = {}
        if not OCCUPATION_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_plow_action(self):
        player = init_player()
        args = {}
        if not PLOW_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(len(player.get_fields()), expected)

    def test_sow_action(self):
        player = init_player()
        player.add_supply(GRAIN, 2)
        player.set_next_space(Field())
        player.breads = 2
        args = {
            GRAIN: 1,
            'bake_bread': 1
        }
        if not SOW_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 2
        self.assertEqual(player.supply[FOOD], expected)
        self.assertEqual(player.supply[GRAIN], 0)
        self.assertEqual(len(player.get_fields()[0].sown), 3)

    def test_plow_sow_action(self):
        player = init_player()
        player.set_next_space(Field())
        player.set_next_space(Field())
        player.add_supply(VEGETABLE)
        player.add_supply(GRAIN, 2)
        args = {
            VEGETABLE: 1,
            GRAIN: 2
        }
        if not PLOW_SOW_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 3
        self.assertEqual(len(player.get_fields()), expected)
        self.assertEqual(sum([len(f.sown) for f in player.get_fields()]), 8)

    def test_bake_bread_action(self):
        player = init_player()
        player.add_supply(GRAIN, 2)
        player.breads = 3
        args = {GRAIN: 2}
        if not BAKE_BREAD_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 6
        self.assertEqual(player.supply[FOOD], expected)

    def test_build_action(self):
        player = init_player()
        player.add_supply(WOOD, 5)
        player.add_supply(REED, 2)
        args = {'stable': 0}
        if not BUILD_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 3
        self.assertEqual(len(player.get_house()), expected)

    def test_fences_action(self):
        player = init_player()
        player.add_supply(WOOD, 7)
        args = {WOOD: 4}
        if not FENCES_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(player.supply[WOOD], 3)
        self.assertEqual(len(player.get_pastures()), expected)

    def test_renovate_action(self):
        player = init_player()
        player.set_next_space(Room(0, WOOD))
        player.set_next_space(Room(0, WOOD))
        player.add_supply(CLAY, 4)
        player.add_supply(REED, 1)
        args = {'material': CLAY}
        if not RENOVATE_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 5
        self.assertEqual(len(player.get_house()), expected)

    def test_child_action(self):
        player = init_player()
        args = {}
        if not CHILD_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 3
        self.assertEqual(player.get_family(), expected)

    def test_child_action2(self):
        player = init_player()
        player.set_next_space(Room(0, WOOD))
        args = {}
        if not CHILD_ACTION2.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 3
        self.assertEqual(player.get_family(), expected)

    def test_major_improvement_action(self):
        player = init_player()
        args = {}
        if not MAJOR_IMPROVEMENT_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_renovate_fences_action(self):
        player = init_player()
        player.add_supply(CLAY, 2)
        player.add_supply(REED, 1)
        player.add_supply(WOOD, 4)
        args = {WOOD: 4, 'material': CLAY}
        if not RENOVATE_FENCES_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 3
        self.assertEqual(len(player.get_house()), expected)
        self.assertEqual(len(player.get_pastures()), 1)

    def test_wood_action(self):
        player = init_player()
        WOOD_ACTION.accumulate()
        if not WOOD_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 3
        self.assertEqual(player.supply[WOOD], expected)

    def test_wood_action2(self):
        player = init_player()
        WOOD_ACTION2.accumulate()
        if not WOOD_ACTION2.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 2
        self.assertEqual(player.supply[WOOD], expected)

    def test_reed_action(self):
        player = init_player()
        REED_ACTION.accumulate()
        if not REED_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(player.supply[REED], expected)

    def test_clay_action(self):
        player = init_player()
        CLAY_ACTION.accumulate()
        CLAY_ACTION.accumulate()
        if not CLAY_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 2
        self.assertEqual(player.supply[CLAY], expected)

    def test_food_action(self):
        player = init_player()
        FOOD_ACTION.accumulate()
        FOOD_ACTION.accumulate()
        FOOD_ACTION.accumulate()
        if not FOOD_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 3
        self.assertEqual(player.supply[FOOD], expected)

    def test_food_action2(self):
        player = init_player()
        if not FOOD_ACTION2.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 2
        self.assertEqual(player.supply[FOOD], expected)

    def test_sheep_action(self):
        player = init_player()
        SHEEP_ACTION.accumulate()
        if not SHEEP_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(player.get_livestock()[SHEEP], expected)

    def test_boar_action(self):
        player = init_player()
        BOAR_ACTION.accumulate()
        if not BOAR_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(player.get_livestock()[BOAR], expected)

    def test_grain_action(self):
        player = init_player()
        if not GRAIN_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(player.supply[GRAIN], expected)

    def test_vegetable_action(self):
        player = init_player()
        if not VEGETABLE_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(player.supply[VEGETABLE], expected)

    def test_cattle_action(self):
        player = init_player()
        CATTLE_ACTION.accumulate()
        if not CATTLE_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(player.get_livestock()[CATTLE], expected)

    def test_stone_action(self):
        player = init_player()
        STONE_ACTION.accumulate()
        STONE_ACTION.accumulate()
        if not STONE_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 2
        self.assertEqual(player.supply[STONE], expected)

    def test_stone_action2(self):
        player = init_player()
        STONE_ACTION2.accumulate()
        if not STONE_ACTION2.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 1
        self.assertEqual(player.supply[STONE], expected)

if __name__ == '__main__':
    unittest.main()
