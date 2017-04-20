from player import *
from action import *
from improvements import MINOR_IMPROVEMENTS


class Game:

    def __init__(self, names):
        self.players = []
        for name in names:
            improvements = MINOR_IMPROVEMENTS[10:17]
            # TODO deal occupations
            occupations = []
            self.players.append(Player(name, improvements, occupations))
        self.actions = START_ACTIONS + shuffle_rounds()
        self.stages = [4, 3, 2, 2, 2, 1]

    def play(self):
        for a in self.actions:
            print a, ':',
        print '\n^^ ACTIONS ^^'
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
                        played = False
                        while not played:
                            played = player.play_action(actions)
                        if played != 'PASSED':
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
    g = Game(['Amelia'])
    g.play()
