from action import *
from player import Player
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
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_sow_action(self):
        player = init_player()
        player.add_supply
        args = {
            'crops': {
                'grains': 1,
                'vegetables': 0
            },
            'bake_bread': 1
        }
        if not SOW_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_plow_sow_action(self):
        player = init_player()
        args = {}
        if not PLOW_SOW_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_bake_bread_action(self):
        player = init_player()
        player.add_supply(GRAIN, 2)
        player.breads = 3
        args = {GRAIN: 2}
        if not BAKE_BREAD_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_build_action(self):
        player = init_player()
        player.add_supply(WOOD, 5)
        player.add_supply(REED, 2)
        args = {}
        if not BUILD_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_fences_action(self):
        player = init_player()
        args = {'woods': 4}
        if not FENCES_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_renovate_action(self):
        player = init_player()
        args = {}
        if not RENOVATE_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_child_action(self):
        player = init_player()
        args = {}
        if not CHILD_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_child_action2(self):
        player = init_player()
        args = {}
        if not CHILD_ACTION2.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_major_improvement_action(self):
        player = init_player()
        args = {}
        if not MAJOR_IMPROVEMENT_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_renovate_fences_action(self):
        player = init_player()
        args = {'woods': 4}
        if not RENOVATE_FENCES_ACTION.apply_action(player, args):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_wood_action(self):
        player = init_player()
        if not WOOD_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_wood_action2(self):
        player = init_player()
        if not WOOD_ACTION2.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_reed_action(self):
        player = init_player()
        if not REED_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_clay_action(self):
        player = init_player()
        if not CLAY_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_food_action(self):
        player = init_player()
        if not FOOD_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_food_action2(self):
        player = init_player()
        if not FOOD_ACTION2.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_sheep_action(self):
        player = init_player()
        if not SHEEP_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_boar_action(self):
        player = init_player()
        if not BOAR_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_grain_action(self):
        player = init_player()
        if not GRAIN_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_vegetable_action(self):
        player = init_player()
        if not VEGETABLE_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_cattle_action(self):
        player = init_player()
        if not CATTLE_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_stone_action(self):
        player = init_player()
        if not STONE_ACTION.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

    def test_stone_action2(self):
        player = init_player()
        if not STONE_ACTION2.apply_action(player, {}):
            self.assertTrue(False, 'Action not completed.')
        expected = 'moo'
        self.assertEqual(player, expected)

if __name__ == '__main__':
    unittest.main()
