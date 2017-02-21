CLAY = 'clay'
STONE = 'stone'
WOOD = 'wood'
REED = 'reed'
FOOD = 'food'
GRAIN = 'grain'
VEGETABLE = 'vegetable'
SHEEP = 'sheep'
BOAR = 'boar'
CATTLE = 'cattle'
PERSON = 'person'

LIVESTOCK = [SHEEP, BOAR, CATTLE]

SCORES = {
    CLAY: [0 for i in range(30)],
    STONE: [0 for i in range(30)],
    WOOD: [0 for i in range(30)],
    REED: [0 for i in range(30)],
    FOOD: [0 for i in range(30)],
    # TODO check all supply scores
    GRAIN: [-1, 1, 1, 1, 2, 2, 3, 3, 4, 4],
    VEGETABLE: [-1] + range(4) + [4 for i in range(25)],
    SHEEP: [-1, 1, 1, 1, 2, 2, 3, 3, 4, 4],
    BOAR: [-1, 1, 1, 2, 2, 3, 3, 4, 4],
    CATTLE: [-1, 1, 1, 2, 2, 3, 3, 4, 4],
    PERSON: [x*3 for x in range(30)],
}
