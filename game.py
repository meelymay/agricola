from player import *
from action import *


class Game:

    def __init__(self, names):
        self.players = [Player(name) for name in names]
        self.actions = START_ACTIONS + shuffle_rounds()
        self.stages = [4, 3, 2, 2, 2, 1]

    def play(self):
        round = len(START_ACTIONS)
        for stage, s in zip(self.stages, range(len(self.stages))):
            for i in range(stage):
                round += 1
                i = round-len(START_ACTIONS)
                print '#################'
                print '###  ROUND %s ###' % (str(i) + (' ' if i < 10 else ''))
                print '#################'
                # setup round
                actions = self.actions[:round]
                for a in actions:
                    a.free()
                    a.accumulate()

                # each player goes in turn
                # until no players have people left
                still_playing = True
                while still_playing:
                    still_playing = False
                    for player in self.players:
                        player.display()
                        if player.play_action(actions):
                            print player, 'played'
                            still_playing = True
                for player in self.players:
                    player.come_home()
            self.harvest(s+1)

    def harvest(self, stage):
        for player in self.players:
            print '&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&'
            print '&~&~&~&~&~&~&~&~&  STAGE   %s  HARVEST &~&~&~&~&~&~&~&~&~&' % stage
            print '&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&~&'
            player.harvest()


if __name__ == '__main__':
    g = Game(['Amelia', 'Dan'])
    g.play()
