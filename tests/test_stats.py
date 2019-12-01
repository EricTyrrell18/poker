#!/usr/bin/env python3


import sys
sys.path.append("../src")

from poker_stats import DeckStatistics

from cards import Suit, Rank
import unittest

class TestDeckStatistics(unittest.TestCase):
    def setUp(self):
        self.deck = DeckStatistics()

    def test_initial_suits_count(self):
        for suit in Suit:
            with self.subTest():
                self.assertEqual(self.deck.suit_count(suit),13)
    def test_initial_ranks_count(self):
        for rank in Rank:
            with self.subTest():
                self.assertEqual(self.deck.rank_count(rank),4)

if __name__ == "__main__":
    unittest.main()
