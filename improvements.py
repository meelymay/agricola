from constants import *


class Improvement:
    def __init__(self, cost, improve, points=0, requirements=[]):
        self.cost = cost
        self.points = points
        self.improve = improve
        self.requirements = requirements

    def name(self):
        return self.improve.__name__

    def apply_instant(self, player):
        self.improve(player)

    def __str__(self):
        points = (' (%s) ' % self.points) if self.points else ''
        prereq = ('PREREQ: %s' % self.requirements) if self.requirements else ''
        return '%s%s: %s\t COST: %s\t%s' % (self.name(), points, self.improve.__doc__, self.cost, prereq)


def fireplace(player):
    player.cooked_food = {
        GRAIN: 1,
        VEGETABLE: 2,
        SHEEP: 2,
        BOAR: 2,
        CATTLE: 3
    }
    player.breads = 2


def hearth(player):
    player.cooked_food = {
        GRAIN: 1,
        VEGETABLE: 3,
        SHEEP: 2,
        BOAR: 3,
        CATTLE: 4
    }
    player.breads = 3


def well(player):
    pass


MAJOR_IMPROVEMENTS = [
    Improvement({CLAY: 2}, fireplace),
    Improvement({CLAY: 3}, fireplace),
    Improvement({CLAY: 4}, hearth),
    Improvement({CLAY: 5}, hearth),
    # TODO add all major improvements
    Improvement({STONE: 2, WOOD: 2}, well, points=4)
]


# MINOR IMPROVEMENTS

def acorn_basket(player):
    '''Place 1 wild boar on each of the next 2 round spaces.'''
    pass

def wool_blankets(player):
    '''During scoring, if you live in a wooden/clay house you get 3/2 bonus points'''
    pass

def milk_jug(player):
    '''Each time any player uses the "Cattle Market" you get 3 food and each other player gets 1 food.'''
    pass

def thick_forest(player):
    '''Place 1 wood on each even numbered round space.'''
    pass

def corn_scoop(player):
    '''Each time you use "Grain Seeds" you get 1 additional grain.'''
    pass

def rammed_clay(player):
    '''Immediately get 1 clay. You can use clay to build fences.'''
    pass

def bread_paddle(player):
    '''Immediately get 1 food. For each occupation you play you get an additional "Bake Bread".'''
    pass

def lumber_mill(player):
    '''Every improvement costs you 1 wood less.'''
    pass

def three_field_rotation(player):
    '''At the start of the field phase of harvest, if you have at least 1 grain field, 1 vegetable field, and 1 empty field, you get 3 food.'''
    pass

def scullery(player):
    '''At the start of each round if you live in a wooden house you get 1 food.'''
    pass

def caravan(player):
    '''This card provides room for 1 person.'''
    pass

def moldboard_plow(player):
    '''Place 2 field tiles on this card. When you use "Farmland" you can also plow 1 field from this card.'''
    pass

def big_country(player):
    '''For each round left to play, you get 1 bonus point and 2 food (now).'''
    pass

def clearing_spade(player):
    '''At any time, you can move 1 crop from a planted field to an empty field.'''
    pass

def dutch_windmill(player):
    '''Each time you "Bake Bread" in a round immediately following a harvest, get an additional 3 food.'''
    pass

def beanfield(player):
    '''A field that can only grow vegetables.'''
    pass

def stone_tongs(player):
    '''Each time you use a stone accumulation space get 1 additional stone.'''
    pass

def loam_pit(player):
    '''Each time you use "Day Laborer" also get 3 clay.'''

    def plus_3_clay(p):
        p.add_supply(CLAY, n=3)

    if DAY_LABORER not in player.after_action:
        player.after_action[DAY_LABORER] = []
    player.after_action[DAY_LABORER].append(plus_3_clay)

def bottles(player):
    '''Costs 1 clay and 1 food per person to play.'''
    pass

def lasso(player):
    '''You can place two people immediately after if at least one uses Sheep, Pig, Cattle'''
    pass

def threshing_board(player):
    '''Each time you use "Farmland" or "Cultivation" you get to "Bake Bread".'''
    pass

def herring_pot(player):
    '''Each time you use "Fishing" place 1 food on each of the next 3 round spaces.'''
    pass

def claypipe(player):
    '''In returning home, if you gained at least 7 building resources, you get 2 food.'''
    pass

def loom(player):
    '''In the field phase, if you have 1/4/7 sheep, you get 1/2/3 food. During scoring you get 1 bonus point for every 3 sheep'''
    pass

def market_stall(player):
    '''Immediately get 1 vegetable.'''
    pass

def large_greenhouse(player):
    '''Place a vegetable on rounds [current round + (4, 7, 9)].'''
    pass

def handplow(player):
    '''Place 1 field tile on round [current round + 5].'''
    pass

def strawberry_patch(player):
    '''Place 1 food on each of the next 3 round spaces.'''
    pass

def carpenters_parlor(player):
    '''Wooden rooms only cost you 2 wood and 2 reed each.'''
    pass

def mantlepiece(player):
    '''Immediately get 1 bonus point for each complete round left to play. You may no longer renovate.'''
    pass

MINOR_IMPROVEMENTS = [
    Improvement({STONE: 1}, mantlepiece, points=-3, requirements={'renovated': True}),
    Improvement({WOOD: 1, STONE: 1}, carpenters_parlor),
    Improvement({WOOD: 1}, strawberry_patch, requirements={'veg_field': 2}, points=2),
    Improvement({WOOD: 1}, handplow),
    Improvement({WOOD: 2}, large_greenhouse, requirements={OCCUPATION: 2}),
    Improvement({GRAIN: 1}, market_stall),
    Improvement({WOOD: 2}, loom, points=1, requirements={OCCUPATION: 2}),
    Improvement({CLAY: 1}, claypipe),
    Improvement({CLAY: 1}, herring_pot),
    Improvement({WOOD: 1}, threshing_board, points=1, requirements={OCCUPATION: 2}),
    Improvement({REED: 1}, lasso),
    Improvement({}, bottles, points=4),
    Improvement({FOOD: 1}, loam_pit, points=1, requirements={OCCUPATION: 3}),
    Improvement({WOOD: 1}, stone_tongs),
    Improvement({FOOD: 1}, beanfield, points=1, requirements={OCCUPATION: 2}),
    Improvement({WOOD: 2, STONE: 2}, dutch_windmill, points=2),
    Improvement({WOOD: 1}, clearing_spade),
    Improvement({}, big_country, requirements={'farmyard': 15}),
    Improvement({WOOD: 2}, moldboard_plow, requirements={OCCUPATION: 1}),
    Improvement({WOOD: 3, FOOD: 3}, caravan),
    Improvement({WOOD: 1, CLAY: 1}, scullery),
    Improvement({REED: 1}, acorn_basket, requirements={OCCUPATION: 3}),
    Improvement({}, wool_blankets, requirements={SHEEP: 5}),
    Improvement({CLAY: 1}, milk_jug),
    Improvement({}, thick_forest, requirements={CLAY: 5}),
    Improvement({WOOD: 1}, corn_scoop),
    Improvement({}, rammed_clay),
    Improvement({WOOD: 1}, bread_paddle),
    Improvement({STONE: 2}, lumber_mill, points=2, requirements={OCCUPATION: -3}),
    Improvement({}, three_field_rotation, requirements={OCCUPATION: 3})
]