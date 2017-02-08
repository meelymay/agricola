class Pasture:
    def __init__(self, name, stable=False):
        # name implies fenced
        self.name = name
        self.stable = stable
        self.livestock = []

    def capacity(self):
        capacity = 1
        if self.name:
            capacity = 2
            if self.stable:
                capacity += 2
        return capacity

    def add_single_livestock(self, livestock):
        if self.livestock:
            if livestock != self.livestock[0]:
                return False
            if len(self.livestock) == self.capacity():
                return False
        self.livestock.append(livestock)
        return True

    def add_livestock(self, livestock, n=1):
        for i in range(n):
            added = self.add_single_livestock(livestock)
            if not added:
                return i
        return n

def shuffle_livestock(pastures, livestock):
    return