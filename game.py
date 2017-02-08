from player import *
from action import *


class Game:

    def __init__(self, names):
        self.players = [Player(name) for name in names]
        self.actions = START_ACTIONS + shuffle(ROUND_ACTIONS)

    def play(self):
        for stage in self.stages:
            for round in stage:
                # setup round
                actions = ACTIONS[:round]
                for a in actions:
                    a.free()
                    a.accumulate()

                # each player goes in turn
                # until no players have people left
                still_playing = True
                while still_playing:
                    still_playing = False
                    for player in self.players:
                        if player.play_action(actions):
                            still_playing = True
                for player in self.players:
                    player.come_home()

if __name__ == '__main__':
    g = Game(['Amelia', 'Dan'])
    g.play()
