import random

from collections import defaultdict

from constants import *
from field import Field
from house import Room
from improvements import MAJOR_IMPROVEMENTS
from pasture import Pasture


TURN_ERROR = '!!!!!!!!    !!!  %s  !!!    !!!!!!!'


class Player:
    def __init__(self, name, improvements, occupations):
        self.name = name

        self.improvements = {}
        for improvement in improvements:
            self.improvements[improvement.name()] = improvement
        self.occupations = occupations

        self.farm = [None for i in range(15)]
        self.farm[0] = Room(1, WOOD)
        self.farm[1] = Room(1, WOOD)
        self.turns = 2

        self.supply = defaultdict(int)

        self.breads = None
        self.pet = None
        self.famines = 0
        self.infants = 0

        self.costs = {
            'room_materials': 5,
            'room_reeds': 2,
            'stable_woods': 2,
            'renovate_reeds': 1
        }

        self.cooked_food = defaultdict(int)
        self.cooked_food[GRAIN] = 1
        self.at_any_time = []
        self.after_action = defaultdict(list)
        self.scoring_bonuses = []

    def check_supply(self, items):
        for item in items:
            if self.supply[item] < items[item]:
                print TURN_ERROR % ('Not enough ' + item)
                return False
        return True

    def come_home(self):
        self.infants = 0
        self.turns = self.get_family()

    def take_action(self, action):
        args = self.specify_action(action)
        return action.apply_action(self, args)

    def play_action(self, actions):
        if not self.turns:
            return 'PASSED'
        acted = False
        while not acted:
            action = self.select_action(actions)
            success = self.take_action(action)
            # TODO make turn errors/failures consistent
            if action in self.after_action:
                for subsequent in self.after_action[action]:
                    subsequent(self)
            acted = True
            # except Exception, e:
            #     print '\n'
            #     print e
            #     print 'Pick another action: '
            if not acted:
                print 'something went wrong....??'
        self.turns -= 1
        return success

    def select_action(self, actions):
        allowed = set([])
        for i in range(len(actions)):
            action = actions[i]
            if not action.occupied:
                allowed.add(i)
            print '%s%s: %s' % ('X' if action.occupied else '', i, action)
        i = -1
        while i not in allowed:
            i = input('Select an action by index: ')
        return actions[i]

    def specify_action(self, action):
        args = {}
        for arg in action.args:
            val = raw_input('Specify %s %s: ' % (action, arg))
            try:
                val = int(val)
            except:
                if val == '':
                    val = 0
            args[arg] = val
        return args

    def get_house(self):
        return [space for space in self.farm if isinstance(space, Room)]

    def get_pasture(self, name):
        return [p for p in self.get_pastures() if p.name == name][0]

    def get_pastures(self):
        return [space for space in self.farm if isinstance(space, Pasture)]

    def get_fields(self):
        return [space for space in self.farm if isinstance(space, Field)]

    def get_family(self):
        return sum([room.people for room in self.get_house()])

    def get_livestock(self):
        all_livestock = defaultdict(int)
        for pasture in self.get_pastures():
            livestock, n = pasture.get_livestock()
            all_livestock[livestock] += n
        if self.pet:
            all_livestock[self.pet] += 1
        return all_livestock

    def get_house_material(self):
        return self.get_house()[0].material

    def set_next_space(self, space):
        for i in range(len(self.farm)):
            if self.farm[i] is None:
                self.farm[i] = space
                return True
        print TURN_ERROR % 'Your farm is full.'
        return False

    def build_room(self, rooms, stables):
        MATERIAL_COST = self.costs['room_materials']
        REED_COST = self.costs['room_reeds']
        STABLE_COST = self.costs['stable_woods']

        material = self.get_house_material()
        total_cost = {
            material: MATERIAL_COST * rooms,
            REED: REED_COST * rooms
        }
        if WOOD not in total_cost:
            total_cost[WOOD] = 0
        total_cost[WOOD] += len(stables) * STABLE_COST
        if not self.check_supply(total_cost):
            return False
        for stable in stables:
            if stable in [p.name for p in self.get_pastures()]:
                self.get_pasture(stable).stable = True
            else:
                name = self.name_new_pasture()
                pasture = Pasture(name, stable=True)
                if not self.set_next_space(pasture):
                    print TURN_ERROR % 'Couldn\'t set a pasture.'
                    return False
        if not self.set_next_space(Room(0, material)):
            # TODO unset pasture
            print TURN_ERROR % 'Couldn\'t set a room???'
            return False
        # TODO balance family if multiple per room
        self.supply[material] -= MATERIAL_COST
        self.supply[REED] -= REED_COST
        for stable in stables:
            self.supply[WOOD] -= STABLE_COST
        return True

    def renovate(self, material):
        REED_COST = self.costs['renovate_reeds']

        if not self.check_supply({
            material: len(self.get_house()),
            REED: REED_COST
        }):
            return False
        self.supply[material] -= len(self.get_house())
        self.supply[REED] -= REED_COST
        self.set_next_space(Room(0, material))
        return True

    def sow(self, crops):
        # check enough fields
        if not self.check_supply(crops):
            return False
        if sum(crops.values()) > [f for f in self.get_fields() if not f.sown]:
            print TURN_ERROR % 'You don\'t have enough empty fields'
            return False
        for crop in crops:
            if crop not in CROPS:
                continue
            n = crops[crop]
            for i in range(n):
                for field in self.get_fields():
                    if not field.sown:
                        field.sow(crop)
                        self.supply[crop] -= 1
                        break
        return True

    def plow(self):
        self.set_next_space(Field())
        return True

    def build_fences(self, woods):
        if not self.check_supply({WOOD: woods}):
            return False

        # TODO most flexible fences building
        existing = len(self.get_pastures())
        name = self.name_new_pasture()
        if woods == 4 and existing != 1:
            if existing == 0:
                self.set_next_space(Pasture(name))
            else:
                self.set_next_space(Pasture(name))
                self.set_next_space(Pasture(name))
        elif woods == 3 and existing > 0:
            self.set_next_space(Pasture(name))
        elif woods == 2 and existing == 3:
            self.set_next_space(Pasture(name))
        elif woods == 5:
            self.set_next_space(Pasture(name))
            name2 = self.name_new_pasture()
            self.set_next_space(Pasture(name2))
        elif woods == 6:
            self.set_next_space(Pasture(name))
            self.set_next_space(Pasture(name))
        elif woods == 7:
            self.set_next_space(Pasture(name))
            name2 = self.name_new_pasture()
            self.set_next_space(Pasture(name2))

        self.supply[WOOD] -= woods
        return True

    def add_child(self, with_room=True):
        house = self.get_house()
        empty_rooms = [room for room in house if room.people == 0]
        if with_room and not empty_rooms:
            print TURN_ERROR % 'You don\'t have room for children'
            return False
        room = empty_rooms[0] if empty_rooms else house[0]
        room.people += 1
        self.infants += 1
        return True

    def add_item(self, item, n=1):
        if item in LIVESTOCK:
            return self.add_livestock(item, n=n)
        return self.add_supply(item, n=n)

    def add_supply(self, item, n=1):
        if n < 0:
            if -n > self.supply[item]:
                return False

        self.supply[item] += n
        return True

    def add_livestock(self, livestock, n=1):
        # TODO remove livestock when n < 0

        # TODO shuffle livestock
        accomodated = 0
        for pasture in self.get_pastures():
            placed = pasture.add_livestock(livestock, n=n)
            n -= placed
            accomodated += placed
            if n == 0:
                return True
        if not self.pet:
            self.pet = livestock
            if n == 1:
                # this was the last one to place
                return True
        print TURN_ERROR % 'Some livestock unplaced.'
        return False

    def bake_bread(self, grains):
        if not self.check_supply({GRAIN: grains}):
            return False
        self.supply[GRAIN] -= grains
        self.supply[FOOD] += grains * self.breads
        return True

    def add_occupation(self, occupation):
        # TODO support occupations
        pass

    def buy_improvement(self, args, major=False):
        improvement_name = args['improvement']

        improvements = self.improvements
        if major:
            for i in MAJOR_IMPROVEMENTS:
                improvements[i.name()] = i
        if improvement_name not in improvements:
            print TURN_ERROR % (improvement_name + ' not in improvements.')
        improvement = improvements[improvement_name]

        if not self.check_supply(improvement.cost):
            return False

        improvement.apply_instant(self)
        for cost in improvement.cost:
            # TODO make paying cost consistent
            self.add_item(cost, n=-improvement.cost[cost])
        del self.improvements[improvement_name]
        return True

    def convert_to_food(self, item):
        if item in LIVESTOCK:
            l = self.get_livestock()
            if item not in l or l[item] == 0:
                print '!!! You do not have %s to convert !!!' % item
                return False
            if self.pet == item:
                self.pet = None
            else:
                for pasture in self.get_pastures():
                    if pasture.livestock_type() == item:
                        pasture.livestock.pop()
                        break
        else:
            if not self.check_supply({item: 1}):
                return False
            self.supply[item] -= 1
        self.supply[FOOD] += self.cooked_food[item]
        return True

    def name_new_pasture(self):
        return 'P%s' % len(self.get_pastures())

    def display(self):
        s = '\n----- Player %s\'s State -----\n' % self.name
        s += 'FARM:\n'
        c = 1
        for space in self.farm:
            s += str(space) + '\t\t'
            if c % 5 == 0:
                s += '\n'
            c += 1
        if self.pet:
            s += 'PET: %s' % self.pet
        s += '\nSUPPLY:\n'
        for item in self.supply:
            s += '\t%s: %s\n' % (item, self.supply[item])
        s += '\nIMPROVEMENTS:\n'
        for improvement in self.improvements.values():
            s += '\t< %s >\n' % improvement
        print s

    def harvest(self):
        # harvest fields
        for field in self.get_fields():
            crops = field.harvest()
            if crops:
                self.add_supply(crops)
        self.display()
        # TODO food stuffs at harvest
        # convert to food
        food_needed = 2*self.get_family() - self.infants
        if self.cooked_food:
            print 'You can cook:'
        for item in self.cooked_food:
            print '\t%s -> %s food' % (item, self.cooked_food[item])
        item = True
        while food_needed > self.supply[FOOD] and item:
            item = raw_input('Which item would you like to cook? ')
            self.convert_to_food(item)
        # eat food
        self.famines += food_needed - self.supply[FOOD]
        self.supply[FOOD] -= min(food_needed, self.supply[FOOD])
        # reproduce animals
        all_livestock = self.get_livestock()
        for livestock in all_livestock:
            if all_livestock[livestock] > 2:
                self.add_livestock(livestock)

    def score(self):
        # famines
        score = -3*self.famines
        # fields
        if len(self.get_fields()) < 2:
            score -= 1
        else:
            score += len(self.get_fields())
        # mega harvest
        for field in self.get_fields():
            if field.sown:
                self.add_supply(field.sown[0], n=len(field.sown))
        # pastures
        # TODO more sophisticated pastures
        score += len(self.get_pastures())
        # fenced stables
        score += len([pasture for pasture in self.get_pastures() if pasture.fenced and pasture.stable])
        # grains
        # vegetables
        for item in supply:
            score += SCORES[item][self.supply[item]]
        # sheep
        # boar
        # cattle
        all_livestock = self.get_livestock()
        for livestock in all_livestock:
            score += SCORES[livestock][all_livestock[livestock]]
        # empty farmland
        score -= len(filter(lambda space: space is None, self.farm))
        # house
        score += SCORES[self.get_house_material()][len(self.get_house())]
        # family
        score += SCORES[PERSON][len(self.get_family())]

        for bonus in scoring_bonuses:
            score += bonus(self)
