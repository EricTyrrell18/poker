#!/usr/bin/env python3

import sys
sys.path.append("../src")

from cards import *
import unittest

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.cards = [card for card in self.deck.deck]
        
    def test_initial_deck_has_52_cards(self):
        """Initial deck should have exactly 52 cards"""
        self.assertEqual(len(self.deck.deck), 52)
    def test_has_correct_number_of_each_rank(self):
   
        ranks = [card.get_rank().name for card in self.cards]

        counts = dict()
        for rank in ranks:
            counts[rank] = counts.get(rank, 0) + 1

        
        self.assertEqual(counts["TWO"], 4)
        self.assertEqual(counts["THREE"], 4)
        self.assertEqual(counts["FOUR"], 4)
        self.assertEqual(counts["FIVE"], 4)
        self.assertEqual(counts["SIX"], 4)
        self.assertEqual(counts["SEVEN"], 4)
        self.assertEqual(counts["EIGHT"], 4)
        self.assertEqual(counts["NINE"], 4)
        self.assertEqual(counts["TEN"], 4)
        self.assertEqual(counts["JACK"], 4)
        self.assertEqual(counts["QUEEN"], 4)
        self.assertEqual(counts["KING"], 4)
        self.assertEqual(counts["ACE"], 4)

    def test_has_correct_number_of_each_suit(self):
        suits = [card.get_suit().name for card in self.cards]

        suit_counter = dict()

        for suit in suits:
            suit_counter[suit] = suit_counter.get(suit, 0) + 1
        self.assertEqual(suit_counter["HEARTS"], 13)
        self.assertEqual(suit_counter["DIAMONDS"], 13)
        self.assertEqual(suit_counter["SPADES"], 13)
        self.assertEqual(suit_counter["CLUBS"], 13)

    def test_deal_card_is_not_none(self):
        card = self.deck.deal_card()
        self.assertEqual(len(self.deck.deck), 51)
        self.assertNotEqual(card, None)

    def test_can_deal_52_cards(self):
        for i in range(52):
            self.deck.deal_card()
        self.assertEqual(len(self.deck.deck), 0)
    def test_throws_error_if_no_cards_left_to_deal(self):
        for i in range(52):
            self.deck.deal_card()
        with self.assertRaises(IndexError):
            self.deck.deal_card()

    def test_deck_after_shuffle_has_52_cards(self):
        test_deck = Deck()
        for i in range(52):
            test_deck.deal_card()
        test_deck.shuffle()
        self.assertEqual(len(test_deck.deck), 52)

    def test_deck_after_shuffle_has_all_ranks(self):
        test_deck = Deck()
        for i in range(52):
            test_deck.deal_card()
        test_deck.shuffle()
    
        ranks = [card.get_rank().name for card in test_deck.deck]

        counts = dict()
        for rank in ranks:
            counts[rank] = counts.get(rank, 0) + 1

        
        self.assertEqual(counts["TWO"], 4)
        self.assertEqual(counts["THREE"], 4)
        self.assertEqual(counts["FOUR"], 4)
        self.assertEqual(counts["FIVE"], 4)
        self.assertEqual(counts["SIX"], 4)
        self.assertEqual(counts["SEVEN"], 4)
        self.assertEqual(counts["EIGHT"], 4)
        self.assertEqual(counts["NINE"], 4)
        self.assertEqual(counts["TEN"], 4)
        self.assertEqual(counts["JACK"], 4)
        self.assertEqual(counts["QUEEN"], 4)
        self.assertEqual(counts["KING"], 4)
        self.assertEqual(counts["ACE"], 4)

    def test_deck_after_shuffle_has_all_suits(self):
        test_deck = Deck()
        for i in range(52):
            test_deck.deal_card()
        test_deck.shuffle()
    
        suits = [card.get_suit().name for card in test_deck.deck]
        suit_counter = dict()

        for suit in suits:
            suit_counter[suit] = suit_counter.get(suit, 0) + 1
        self.assertEqual(suit_counter["HEARTS"], 13)
        self.assertEqual(suit_counter["DIAMONDS"], 13)
        self.assertEqual(suit_counter["SPADES"], 13)
        self.assertEqual(suit_counter["CLUBS"], 13)


if __name__ == "__main__":
    unittest.main()


