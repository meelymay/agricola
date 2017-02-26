from constants import *
import random


class Action:
    def __init__(self, resource=None, special=None, accumulation=0, count=0, args=[]):
        if not resource and not special:
            raise Exception('Action must have a resource or a special action.')
        self.resource = resource
        self.count = count
        self.special = special
        self.accumulation = accumulation
        self.occupied = False
        self.args = args

    def apply_action(self, player, args):
        if self.occupied:
            raise Exception('Action already occupied.')

        self.occupied = True
        if self.resource:
            acquired = player.add_item(self.resource, self.count or 1)
            if acquired and self.accumulation:
                self.count = 0
            return acquired
        else:
            return self.special(player, args)

    def accumulate(self):
        self.count += self.accumulation

    def free(self):
        self.occupied = False

    def __str__(self):
        if self.resource:
            plus = '+' if not self.accumulation else 'get'
            return '%s %s %s' % (plus, self.count, self.resource)
        else:
            return self.special.__name__

def occupation_action(player, occupation):
    return player.add_occupation(occupation)

def plow_action(player, n):
    return player.plow()

def sow_action(player, args):
    if player.sow(args['crops']):
        return player.bake_bread(args['bake_bread'])
    else:
        return False

def plow_sow_action(player, crops):
    player.plow()
    return player.sow(crops)

def bake_bread_action(player, args):
    return player.bake_bread(args[GRAIN])

def build_action(player, stable):
    return player.build_room(stable)

def fences_action(player, woods):
    return player.build_fences(woods)

def renovate_action(player, args):
    return player.renovate()

def child_action(player, args):
    return player.add_child()

def child_action2(player, args):
    return player.add_child(with_room=False)

def major_improvement_action(player, improvement):
    return player.buy_major_improvement(improvement)

def renovate_fences_action(player, args):
    if player.renovate():
        return fences_action(player, args['woods'])
    else:
        False

def meeting_action(player, improvement):
    # TODO change who's first
    return player.buy_improvement(improvement)

OCCUPATION_ACTION = Action(special=occupation_action, args=['occupation'])
PLOW_ACTION = Action(special=plow_action)
SOW_ACTION = Action(special=sow_action, args=['bake_bread', 'crops'])
PLOW_SOW_ACTION = Action(special=plow_sow_action, args=['crops'])
BAKE_BREAD_ACTION = Action(special=bake_bread_action, args=['bake_bread'])
BUILD_ACTION = Action(special=build_action, args=['stable'])
FENCES_ACTION = Action(special=fences_action, args=['woods'])
RENOVATE_ACTION = Action(special=renovate_action)
CHILD_ACTION = Action(special=child_action)
CHILD_ACTION2 = Action(special=child_action2)
MAJOR_IMPROVEMENT_ACTION = Action(special=major_improvement_action, args=['improvement'])
RENOVATE_FENCES_ACTION = Action(special=renovate_fences_action, args=['fences'])
MEETING_ACTION = Action(special=meeting_action, args=['improvement'])

WOOD_ACTION = Action(resource=WOOD, accumulation=3)
WOOD_ACTION2 = Action(resource=WOOD, accumulation=2)
REED_ACTION = Action(resource=REED, accumulation=1)
CLAY_ACTION = Action(resource=CLAY, accumulation=1)
FOOD_ACTION = Action(resource=FOOD, accumulation=1)
FOOD_ACTION2 = Action(resource=FOOD, count=2)
SHEEP_ACTION = Action(resource=SHEEP, accumulation=1)
BOAR_ACTION = Action(resource=BOAR, accumulation=1)
GRAIN_ACTION = Action(resource=GRAIN, count=1)
VEGETABLE_ACTION = Action(resource=VEGETABLE, count=1)
CATTLE_ACTION = Action(resource=CATTLE, accumulation=1)
STONE_ACTION = Action(resource=STONE, accumulation=1)
STONE_ACTION2 = Action(resource=STONE, accumulation=1)

START_ACTIONS = [
    OCCUPATION_ACTION,
    WOOD_ACTION,
    REED_ACTION,
    FOOD_ACTION,
    FOOD_ACTION2,
    CLAY_ACTION,
    PLOW_ACTION,
    GRAIN_ACTION,
    BUILD_ACTION,
    MEETING_ACTION
]

ROUND_ACTIONS = [
    [
        SHEEP_ACTION,
        MAJOR_IMPROVEMENT_ACTION,
        SOW_ACTION,
        FENCES_ACTION
    ], [
        STONE_ACTION,
        VEGETABLE_ACTION,
        CHILD_ACTION
    ], [
        RENOVATE_ACTION,
        BOAR_ACTION
    ], [
        CATTLE_ACTION,
        STONE_ACTION
    ], [
        CHILD_ACTION2,
        PLOW_SOW_ACTION
    ],
    [RENOVATE_FENCES_ACTION]
]

def shuffle_rounds():
    actions = []
    for stage in ROUND_ACTIONS:
        stage = stage[:]
        while stage:
            action = random.choice(stage)
            stage.remove(action)
            actions.append(action)
    return actions
