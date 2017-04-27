import action

from constants import *


def gen_supply_add(item, n):
    def supply_add(player):
        p.add_supply(item, n=n)
    return supply_add


class Improvement:
    def __init__(self, cost, improve, points=0, requirements=[], space_bonus={}, game=None):
        self.cost = cost
        self.points = points
        self.improve = improve
        self.requirements = requirements
        self.game = game
        self.space_bonus = space_bonus

    def name(self):
        return self.improve.__name__

    def apply_instant(self, player):
        player.scoring_bonuses.append(lambda p: self.points)
        for space in self.space_bonus:
            self.game.add_bonus(player, space, self.space_bonus[space])
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
    # TODO place on round spaces
    pass

def wool_blankets(player):
    '''During scoring, if you live in a wooden/clay house you get 3/2 bonus points'''

    def unrenovated_bonus(player):
        material = player.get_house_material()
        if material == WOOD:
            return 3
        elif material == CLAY:
            return 2
        else:
            return 0

    player.scoring_bonuses.append(unrenovated_bonus)

def milk_jug(player, other_players):
    '''Each time any player uses the "Cattle Market" you get 3 food and each other player gets 1 food.'''
    player.after_action[action.CATTLE_ACTION].append(gen_supply_add(FOOD, 3))
    # TODO cattle market for other_players (both ways)

def thick_forest(player):
    '''Place 1 wood on each even numbered round space.'''
    pass

def corn_scoop(player):
    '''Each time you use "Grain Seeds" you get 1 additional grain.'''
    player.after_action[action.GRAIN_SEEDS].append(gen_supply_add(GRAIN, 1))

def rammed_clay(player):
    '''Immediately get 1 clay. You can use clay to build fences.'''
    # TODO clay for fences?!
    pass

def bread_paddle(player):
    '''Immediately get 1 food. For each occupation you play you get an additional "Bake Bread".'''
    player.after_action[action.OCCUPATION_ACTION].append(lambda p: p.take_action(action.BAKE_BREAD))

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
    player.after_action[action.STONE_ACTION].append(gen_supply_add(STONE, 1))
    player.after_action[action.STONE_ACTION2].append(gen_supply_add(STONE, 1))

def loam_pit(player):
    '''Each time you use "Day Laborer" also get 3 clay.'''
    if action.DAY_LABORER not in player.after_action:
        player.after_action[action.DAY_LABORER] = []
    player.after_action[action.DAY_LABORER].append(gen_supply_add(CLAY, 3))

def bottles(player):
    '''Costs 1 clay and 1 food per person to play.'''
    # DONE
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

def init_minors(game):
    return [
        Improvement({STONE: 1}, mantlepiece, points=-3, requirements={'renovated': True}, game=game),
        Improvement({WOOD: 1, STONE: 1}, carpenters_parlor, game=game),
        Improvement({WOOD: 1}, strawberry_patch, requirements={'veg_field': 2}, points=2, game=game),
        Improvement({WOOD: 1}, handplow, game=game),
        Improvement({WOOD: 2}, large_greenhouse, requirements={OCCUPATION: 2}, game=game),
        Improvement({GRAIN: 1}, market_stall, game=game),
        Improvement({WOOD: 2}, loom, points=1, requirements={OCCUPATION: 2}, game=game),
        Improvement({CLAY: 1}, claypipe, game=game),
        Improvement({CLAY: 1}, herring_pot, game=game),
        Improvement({WOOD: 1}, threshing_board, points=1, requirements={OCCUPATION: 2}, game=game),
        Improvement({REED: 1}, lasso, game=game),
        Improvement({}, bottles, points=4, game=game),
        Improvement({FOOD: 1}, loam_pit, points=1, requirements={OCCUPATION: 3}, game=game),
        Improvement({WOOD: 1}, stone_tongs, game=game),
        Improvement({FOOD: 1}, beanfield, points=1, requirements={OCCUPATION: 2}, game=game),
        Improvement({WOOD: 2, STONE: 2}, dutch_windmill, points=2, game=game),
        Improvement({WOOD: 1}, clearing_spade, game=game),
        Improvement({}, big_country, requirements={'farmyard': 15}, game=game),
        Improvement({WOOD: 2}, moldboard_plow, requirements={OCCUPATION: 1}, game=game),
        Improvement({WOOD: 3, FOOD: 3}, caravan, game=game),
        Improvement({WOOD: 1, CLAY: 1}, scullery, game=game),
        Improvement({REED: 1}, acorn_basket, requirements={OCCUPATION: 3}, space_bonus={
            1: [BOAR],
            2: [BOAR]
        }, game=game),
        Improvement({}, wool_blankets, requirements={SHEEP: 5}, game=game),
        Improvement({CLAY: 1}, milk_jug, game=game),
        Improvement({}, thick_forest, requirements={CLAY: 5}, game=game),
        Improvement({WOOD: 1}, corn_scoop, game=game),
        Improvement({}, rammed_clay, game=game),
        Improvement({WOOD: 1}, bread_paddle, game=game),
        Improvement({STONE: 2}, lumber_mill, points=2, requirements={OCCUPATION: -3}, game=game),
        Improvement({}, three_field_rotation, requirements={OCCUPATION: 3}, game=game)
    ]