#!/usr/bin/env python3
"""
Tests the functionality of the evaluator
Requires that you create a Hand db in this directory
You can uncomment the code in __main__ to do this
Just be sure to recomment it
"""
import sys
sys.path.append("../src/")

import os
import unittest
from texas_holdem import TexasHandEvaluator
from cards import Card, Deck, Rank, Suit
from create_hand_dict import FiveCardGenerator
class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = TexasHandEvaluator()

        """
        List of hands for testing.
        The worst of each type of  hand is first and the best is second
        0 - 1: High Card
        2 - 3: Pairs
        4 - 5: Two Pairs
        6 - 7: Three of a Kind
        8 - 9: Straight
        10 - 11: Flush
        12 - 13: Full House
        14 - 15: Four of a Kind
        16 - 17: Straight FLush
        """
        self.testing_hands = [(Card(Rank.TWO,Suit.HEARTS), Card(Rank.THREE,Suit.HEARTS),Card(Rank.FOUR,Suit.SPADES),Card(Rank.SIX,Suit.HEARTS),Card(Rank.SEVEN,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.KING,Suit.SPADES),Card(Rank.QUEEN,Suit.HEARTS),Card(Rank.JACK,Suit.HEARTS),Card(Rank.NINE,Suit.HEARTS),),
                        (Card(Rank.TWO,Suit.HEARTS), Card(Rank.TWO,Suit.SPADES),Card(Rank.THREE,Suit.HEARTS),Card(Rank.FOUR,Suit.HEARTS),Card(Rank.FIVE,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.ACE,Suit.SPADES),Card(Rank.KING,Suit.HEARTS),Card(Rank.QUEEN,Suit.HEARTS),Card(Rank.JACK,Suit.HEARTS),),
                        (Card(Rank.TWO,Suit.HEARTS), Card(Rank.TWO,Suit.SPADES),Card(Rank.THREE,Suit.HEARTS),Card(Rank.THREE,Suit.SPADES),Card(Rank.FOUR,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.ACE,Suit.SPADES),Card(Rank.KING,Suit.HEARTS),Card(Rank.KING,Suit.SPADES),Card(Rank.QUEEN,Suit.HEARTS),),
                        (Card(Rank.TWO,Suit.HEARTS), Card(Rank.TWO,Suit.SPADES),Card(Rank.TWO,Suit.CLUBS),Card(Rank.THREE,Suit.HEARTS),Card(Rank.FOUR,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.ACE,Suit.SPADES),Card(Rank.ACE,Suit.CLUBS),Card(Rank.KING,Suit.HEARTS),Card(Rank.QUEEN,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.TWO,Suit.SPADES),Card(Rank.THREE,Suit.HEARTS),Card(Rank.FOUR,Suit.HEARTS),Card(Rank.FIVE,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.KING,Suit.HEARTS),Card(Rank.QUEEN,Suit.SPADES),Card(Rank.JACK,Suit.HEARTS),Card(Rank.TEN,Suit.HEARTS),),
                        (Card(Rank.TWO,Suit.HEARTS), Card(Rank.THREE,Suit.HEARTS),Card(Rank.FOUR,Suit.HEARTS),Card(Rank.FIVE,Suit.HEARTS),Card(Rank.SEVEN,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.KING,Suit.HEARTS),Card(Rank.QUEEN,Suit.HEARTS),Card(Rank.JACK,Suit.HEARTS),Card(Rank.NINE,Suit.HEARTS),),
                        (Card(Rank.TWO,Suit.HEARTS), Card(Rank.TWO,Suit.SPADES),Card(Rank.TWO,Suit.DIAMONDS),Card(Rank.THREE,Suit.HEARTS),Card(Rank.THREE,Suit.SPADES),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.ACE,Suit.SPADES),Card(Rank.ACE,Suit.CLUBS),Card(Rank.KING,Suit.HEARTS),Card(Rank.KING,Suit.SPADES),),
                        (Card(Rank.TWO,Suit.HEARTS), Card(Rank.TWO,Suit.SPADES),Card(Rank.TWO,Suit.CLUBS),Card(Rank.TWO,Suit.DIAMONDS),Card(Rank.THREE,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.ACE,Suit.SPADES),Card(Rank.ACE,Suit.CLUBS),Card(Rank.ACE,Suit.DIAMONDS),Card(Rank.KING,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.TWO,Suit.HEARTS),Card(Rank.THREE,Suit.HEARTS),Card(Rank.FOUR,Suit.HEARTS),Card(Rank.FIVE,Suit.HEARTS),),
                        (Card(Rank.ACE,Suit.HEARTS), Card(Rank.KING,Suit.HEARTS),Card(Rank.QUEEN,Suit.HEARTS),Card(Rank.JACK,Suit.HEARTS),Card(Rank.TEN,Suit.HEARTS),)]
        


    def test_hand_hierarchy_is_correct(self):
        """Test that all hands are better than every hand below them"""
        for i in range(1,len(self.testing_hands)):
            hand1 = self.testing_hands[i]
            for j in range(i):
                hand2 = self.testing_hands[j]
                self.assertTrue(self.evaluator.evaluate_hand(hand1) >self.evaluator.evaluate_hand(hand2))  
               


if __name__ == "__main__":
    #db_creator = FiveCardGenerator()
    #db_creator.create_hand_db()
    #db_creator.save_hand_db()
    unittest.main()
