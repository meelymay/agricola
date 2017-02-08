from constants import *


class Action:
    def __init__(self, resource=None, special=None, accumulation=0, count=0):
        if not resource and not special:
            raise Exception('Action must have a resource or a special action.')
        self.resource = resource
        self.count = count
        self.special = special
        self.accumulation = accumulation

    def apply_action(self, player, args):
        if self.resource:
            return player.add_item(self.resource, self.count or 1)
        else:
            return self.special(player, args)

    def accumulate(self):
        self.resources += self.accumulation


def occupation_action(player, occupation):
    return player.add_occupation(occupation)

def plow_action(player, n):
    return player.plow(n)

def sow_action(player, crops):
    return player.sow(crops)

def plow_sow_action(player, args):
    n, crops = args
    player.plow(n)
    return player.sow(crops)

def bake_bread_action(player, n):
    return player.bake_bread(n)

def build_action(player, stable):
    return player.build_room(stable)

def build_fences_action(player, woods):
    return player.build_fences(woods)

def renovate_action(player, args):
    return player.renovate()

def child_action(player, args):
    return player.add_child()

def child_action2(player, args):
    return player.add_child(with_room=False)

OCCUPATION_ACTION = Action(special=occupation_action)
PLOW_ACTION = Action(special=plow_action)
SOW_ACTION = Action(special=sow_action)
PLOW_SOW_ACTION = Action(special=plow_sow_action)
BAKE_BREAD_ACTION = Action(special=bake_break)
BUILD_ACTION = Action(special=build_action)
FENCES_ACTION = Action(special=fences_action)
RENOVATE_ACTION = Action(special=renovate_action)
CHILD_ACTION = Action(special=child_action)
CHILD_ACTION2 = Action(special=child_action2)

WOOD_ACTION = Action(resource=WOOD, accumulation=3)
WOOD_ACTION2 = Action(resource=WOOD, accumulation=2)
REED_ACTION = Action(resource=REED, accumulation=1)
FOOD_ACTION = Action(resource=FOOD, accumulation=1)
FOOD_ACTION2 = Action(resource=FOOD, count=2)
SHEEP_ACTION = Action(resource=SHEEP, accumulation=1)
BOAR_ACTION = Action(resource=BOAR, accumulation=1)
GRAIN_ACTION = Action(resource=GRAIN)
VEGETABLE_ACTION = Action(resource=VEGETABLE)
CATTLE_ACTION = Action(resource=CATTLE, accumulation=1)
STONE_ACTION = Action(resource=STONE, accumulation=1)
STONE_ACTION2 = Action(resource=STONE, accumulation=1)

START_ACTIONS = {
    '': OCCUPATION_ACTION,
    '': WOOD_ACTION,
    '': REED_ACTION,
}

STAGES = [
[],
[]
]