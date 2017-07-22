import unittest

from elo import Match
from random import randint


class TestElo(unittest.TestCase):

    def test_elo_preserving(self):
        match = Match()
        for i in range(2, 5):

            match.add_player(str(i), i, randint(500, 3000))

        match.calculate_elo()

        elo_pre = sum([p.elo_pre for p in match.players])
        elo_post = sum([p.elo_post for p in match.players])

        self.assertAlmostEqual(elo_pre, elo_post, msg=f"Elo is not preserved! "
                                                      f"Elo was changed from {elo_pre} to {elo_post} "
                                                      f"with {i} players")

    def test_2player_match(self):
        """ Testing matches with 2 player.
        Tests if weak player against strong player, with weak player winning
        gains more elo than strong player winning against weak player.
        """
        match = Match()

        # simulate two player game with the weaker player winning the game

        elo_a = randint(1000, 3000)
        match.add_player("a", 1, elo_a)
        match.add_player("b", 2, elo_a+randint(100, 500))
        match.calculate_elo()

        # player a should win elo
        self.assertGreaterEqual(match.players[0].elo_post, match.players[0].elo_pre)
        # player b should loose elo
        self.assertGreaterEqual(match.players[1].elo_pre, match.players[1].elo_post)

        elochange_a_match1 = match.get_elo_change("a")

        # resetting match
        match = Match()

        # simulate two player game with the stronger player winning the game
        elo_a = randint(1000, 3000)
        match.add_player("a", 1, elo_a)
        match.add_player("b", 2, elo_a-randint(100, 500))
        match.calculate_elo()

        # player a should win elo
        self.assertGreaterEqual(match.players[0].elo_post, match.players[0].elo_pre)
        # player b should loose elo
        self.assertGreaterEqual(match.players[1].elo_pre, match.players[1].elo_post)

        elochange_a_match2 = match.get_elo_change("a")
        # elochange in first match should be greater than in second match, since in second match
        # the outcome was expected

        self.assertGreater(elochange_a_match1, elochange_a_match2)
