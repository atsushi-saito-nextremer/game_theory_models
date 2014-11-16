"""
Filename: test_game_tools.py
Author: Daisuke Oyama

Tests for game_tools.py

"""
from __future__ import division

import numpy as np
from numpy.testing import assert_array_equal
import nose
from nose.tools import eq_, ok_

from game_tools import Player, NormalFormGame, br_correspondence


class TestPlayer_1opponent:
    """Test the methods of Player with one opponent player"""

    def setUp(self):
        """Setup a Player instance"""
        coordination_game_matrix = [[4, 0], [3, 2]]
        self.player = Player(coordination_game_matrix)

    def test_best_response_against_pure(self):
        """best_response against a pure action"""
        eq_(self.player.best_response(1), 1)

    def test_best_response_against_mixed(self):
        """best_response against a mixed action"""
        eq_(self.player.best_response([1/2, 1/2]), 1)

    def test_best_response_list_when_tie(self):
        """best_response with tie_breaking=False"""
        assert_array_equal(
            sorted(self.player.best_response([2/3, 1/3], tie_breaking=False)),
            sorted([0, 1])
        )

    def test_best_response_with_tie_breaking(self):
        """best_response with tie_breaking=True (default)"""
        ok_(self.player.best_response([2/3, 1/3]) in [0, 1])

    def test_is_best_response_pure(self):
        """is_best_response with pure actions"""
        ok_(self.player.is_best_response(0, 0))

    def test_is_best_response_mixed(self):
        """is_best_response with mixed actions"""
        ok_(self.player.is_best_response([1/2, 1/2], [2/3, 1/3]))


class TestPlayer_2opponents:
    """Test the methods of Player with two opponent players"""

    def setUp(self):
        """Setup a Player instance"""
        payoffs_2opponents = [[[3, 6],
                               [4, 2]],
                              [[1, 0],
                               [5, 7]]]
        self.player = Player(payoffs_2opponents)

    def test_best_response_against_pure(self):
        """best_response against a pure action"""
        eq_(self.player.best_response((1, 1)), 1)

    def test_best_response_list_when_tie(self):
        """best_response with tie_breaking=False"""
        assert_array_equal(
            sorted(self.player.best_response(([3/7, 4/7], [1/2, 1/2]),
                                             tie_breaking=False)),
            sorted([0, 1])
        )


class TestNormalFormGame_Sym2p:
    """Test the methods of NormalFormGame with symmetric two players"""

    def setUp(self):
        """Setup a NormalFormGame instance"""
        coordination_game_matrix = [[4, 0], [3, 2]]
        self.g = NormalFormGame(coordination_game_matrix)

    def test_is_nash_pure(self):
        """is_nash with pure actions"""
        ok_(self.g.is_nash((0, 0)))

    def test_is_nash_mixed(self):
        """is_nash with mixed actions"""
        ok_(self.g.is_nash(([2/3, 1/3], [2/3, 1/3])))


class TestNormalFormGame_Asym2p:
    """Test the methods of NormalFormGame with asymmetric two players"""

    def setUp(self):
        """Setup a NormalFormGame instance"""
        matching_pennies_bimatrix = [[( 1, -1), (-1,  1)],
                                     [(-1,  1), ( 1, -1)]]
        self.g = NormalFormGame(matching_pennies_bimatrix)

    def test_is_nash_pure(self):
        """is_nash with pure actions"""
        ok_(not self.g.is_nash((0, 0)))

    def test_is_nash_mixed(self):
        """is_nash with mixed actions"""
        ok_(self.g.is_nash(([1/2, 1/2], [1/2, 1/2])))


def test_normalformgame_construction_action_sizes():
    g = NormalFormGame((2, 3, 4))

    eq_(g.N, 3)  # Number of players

    assert_array_equal(
        g.players[0].payoff_array,
        np.zeros((2, 3, 4))
    )
    assert_array_equal(
        g.players[1].payoff_array,
        np.zeros((3, 4, 2))
    )
    assert_array_equal(
        g.players[2].payoff_array,
        np.zeros((4, 2, 3))
    )


if __name__ == '__main__':
    import sys

    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)
