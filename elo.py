""" All elo calculations are done here.
Some parts copied from https://github.com/FigBug/Multiplayer-ELO/blob/master/python/elo.py

modified by Dimitri Wessels
"""

from typing import List


class Player:
    def __init__(self, name, place, elo):

        # both for easier correctness and for automatic type hinting
        assert isinstance(name, str)
        place = int(place)
        elo = float(elo)

        self.name = name
        self.place = place
        self.elo_pre = elo

        # internal state used for calculations by Match.calculate_elo
        self.elo_post = 0
        self.elo_change = 0

    def __eq__(self, other):
        return self.name == other.name


class Match:

    def __init__(self):
        self.players: List[Player] = []

    def add_player(self, name, place, elo):
        player = Player(name, place, elo)
        self.players.append(player)

    def get_elo(self, name):
        for player in self.players:
            if player.name == name:
                return player.eloPost
        return 1500  # 1500 is default elo for an unknown player.

    def get_elo_change(self, name):
        for p in self.players:
            if p.name == name:
                return p.elo_change
        return 0

    def calculate_elo(self):
        n = len(self.players)
        k = 32 / (n - 1)

        for player in self.players:
            curplace = player.place
            curelo = player.elo_pre

            for opponent in self.players:
                if player != opponent:
                    opponentplace = opponent.place
                    opponentelo = opponent.elo_pre

                    # main change of algorithm, we just look at 1v1 matches
                    if curplace < opponentplace:
                        score = 1.0
                    elif curplace == opponentplace:
                        score = 0.5
                    else:
                        score = 0.0

                    # work out expected_score
                    expected_score = 1 / (1.0 + 10.0 ** ((opponentelo - curelo) / 400.0))

                    # calculate ELO change vs this one opponent, add it to our change bucket
                    player.elo_change += k * (score - expected_score)

            # add accumulated change to initial ELO for final ELO
            player.elo_post = player.elo_pre + player.elo_change


if __name__ == '__main__':
    match = Match()

    match.add_player("dimitri", 1, 1000)
    match.add_player("max", 3, 1200)
    match.add_player("lukbö", 3, 1000)
    match.add_player("lukbö2", 3, 1000)

    match.calculate_elo()
    for p in match.players:

        print(f'{p.name}: {p.elo_pre} -> {p.elo_post}, changed: {p.elo_change}')
    elo_pre = sum([p.elo_pre for p in match.players])
    elo_post = sum([p.elo_post for p in match.players])

    print(f'EloPre: {elo_pre}, EloPost: {elo_post}')
    print('#'*100)
    print()
