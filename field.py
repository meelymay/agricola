from constants import GRAIN, VEGETABLE

PER_CROP = {
    GRAIN: 3,
    VEGETABLE: 2
}


class Field:
    def __init__(self):
        self.sown = []

    def sow(self, crop):
        self.sown = [crop]*PER_CROP[crop]

    def harvest(self):
        return self.sown.pop() if self.sown else None
