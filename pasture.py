class Pasture:
    def __init__(self, name, stable=False):
        # name implies fenced
        self.name = name
        self.stable = stable
        self.livestock = []

    def capacity(self):
        capacity = 1
        if self.name:
            # TODO somehow unfences stables are getting named?
            capacity = 2
            if self.stable:
                capacity += 2
        return capacity

    def livestock_type(self):
        if not self.livestock:
            return None
        return self.livestock[0]

    def add_single_livestock(self, livestock):
        if self.livestock:
            if livestock != self.livestock[0]:
                return False
            if len(self.livestock) == self.capacity():
                return False
        self.livestock.append(livestock)
        return True

    def get_livestock(self):
        return (self.livestock_type(), len(self.livestock))

    def add_livestock(self, livestock, n=1):
        for i in range(n):
            added = self.add_single_livestock(livestock)
            if not added:
                return i
        return n

    def __str__(self):
        return 'Pasture %s: %s %s %s' % (
            self.name,
            self.livestock_type() or '',
            len(self.livestock) or 'empty',
            'stable' if self.stable else ''
        )

def shuffle_livestock(pastures, livestock):
    return