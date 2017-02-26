from collections import defaultdict
from house import Room
from pasture import Pasture
from field import Field
from constants import *
import random


class Player:
    def __init__(self, name):
        self.name = name
        self.farm = [None for i in range(15)]
        self.farm[0] = Room(1, WOOD)
        self.farm[1] = Room(1, WOOD)
        self.supply = defaultdict(int)
        self.pet = None
        self.famines = 0
        self.turns = 2

    def come_home(self):
        self.turns = self.get_family()

    def play_action(self, actions):
        if not self.turns:
            return False
        acted = False
        while not acted:
            action = self.select_action(actions)
            args = self.specify_action(action)
            try:
                success = action.apply_action(self, args)
                acted = True
            except Exception, e:
                print '\n'
                print e
                print 'Pick another action: '
        self.turns -= 1
        print 'success?', success
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
            args[arg] = val
        return args

    def get_house(self):
        return [space for space in self.farm if isinstance(space, Room)]

    def get_pasture(self, name):
        return [p for p in self.get_pastures() if p.name == name]

    def get_pastures(self):
        return [space for space in self.farm if isinstance(space, Pasture)]

    def get_fields(self):
        return [space for space in self.farm if isinstance(space, Field)]

    def get_family(self):
        return sum([room.people for room in self.get_house()])

    def set_next_space(self, space):
        for i in range(len(self.farm)):
            if self.farm[i] is None:
                self.farm[i] = space
                return True
        return False

    def get_livestock(self):
        all_livestock = defaultdict(int)
        for pasture in self.get_pastures():
            livestock, n = pasture.get_livestock()
            all_livestock[livestock] += n
        if self.pet:
            all_livestock[self.pet] += 1
        return all_livestock

    def build_room(self, stable):
        MATERIAL_COST = 5
        REED_COST = 2
        STABLE_COST = 2

        material = self.get_house()[0].material
        stable_cost = 2 + (5 if material == WOOD else 0)
        if (self.supply[material] < MATERIAL_COST or
           self.supply[REED] < REED_COST or
           (stable and self.supply[WOOD] < stable_cost)):
            return False
        if stable:
            if stable['pasture_name']:
                self.get_pasture(stable['pasture_name']).stable = True
            else:
                name = self.name_new_pasture()
                pasture = Pasture(name, stable=True)
                if not self.set_next_space(pasture):
                    return False
        if not self.set_next_space(Room(0, material)):
            # TODO unset pasture
            return False
        # TODO balance family if multiple per room
        self.supply[material] -= MATERIAL_COST
        self.supply[material] -= REED_COST
        if stable:
            self.supply[WOOD] -= STABLE_COST
        return True

    def renovate(self):
        return True

    def sow(self, crops):
        # check enough fields
        if len(crops) > [f for f in self.get_fields() if not f.sown]:
            return False
        for crop in crops:
            for field in self.get_fields():
                if not field.sown:
                    field.sow(crop)
        return True

    def plow(self):
        self.set_next_space(Field())
        return True

    def build_fences(self, woods):
        if woods == 4:
            name = self.name_new_pasture()
            self.set_next_space(Pasture(name))
        # TODO guh fences
        return True

    def add_child(self, with_room=True):
        house = self.get_house()
        empty_rooms = [room for room in house if room.people == 0]
        if with_room:
            if empty_rooms:
                return False
        room = empty_rooms[0] if empty_rooms else house[0]
        room.people += 1
        return True

    def add_item(self, item, n=1):
        if item in LIVESTOCK:
            return self.add_livestock(item, n=n)
        return self.add_supply(item, n=n)

    def add_supply(self, item, n=1):
        self.supply[item] += n
        return True

    def add_livestock(self, livestock, n=1):
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
        return False

    def bake_bread(self, grains):
        if grains > self.supply[GRAIN]:
            return False
        self.supply[GRAIN] -= grains
        self.supply[FOOD] += grains * self.breads
        return True

    def add_occupation(self, occupation):
        # TODO support occupations
        pass

    def buy_major_improvement(self, improvement):
        # TODO support major improvements
        self.breads = 2
        return False

    def buy_minor_improvement(self, improvement):
        # TODO support minor improvements
        pass

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
        s += '\nITEMS:\n'
        for item in self.supply:
            s += '\t%s: %s\n' % (item, self.supply[item])
        print s

    def harvest(self):
        # harvest fields
        for field in self.fields():
            self.add_supply(field.harvest())
        # TODO food stuffs at harvest
        # convert to food
        # eat food
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
        score += SCORES[self.get_house()[0].material][len(self.get_house())]
        # family
        score += SCORES[PERSON][len(self.get_family())]
