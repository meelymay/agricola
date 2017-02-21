class Room:
    def __init__(self, people, material):
        self.people = people
        self.material = material

    def __str__(self):
        return 'House (%s): %s' % (self.material, self.people)
