#!/usr/bin/env python
import sys
import pickle
from functools import reduce
from cards import Suit
class TexasHandEvaluator():
    
    def __init__(self):
        self.load_hand_db()
        #print(self.hand_rankings)
    def load_hand_db(self):
        f = open("handDB.pkl", "rb")
        self.hand_rankings = pickle.load(f)
        f.close()
    
    def hash_hand(self, hand):
        return reduce(lambda x,y: x*y, [card.rank.value for card in hand] )

    def evaluate_hand(self, hand):
        # Return the rank of the given hand 
        hand_hash = self.hash_hand(hand)
        
        hand_rank = self.hand_rankings[hand_hash]
        # 5863

        if self.is_flush(hand):
            # This actually works for both regular and straight flushes
            # Probably needs testing to make sure it works perfectly for the edges 
            # 5863 is the AKQJ10
            # 7141 is the first Full house
            # 1 is the first high card
            # 1 + 5863 = 5864: GOOD
            # 1277 is the last high card
            # 1277 + 5863 = 7140 : GOOD
            # straights will also work

            hand_rank += 5863
        return hand_rank

    def is_flush(self, hand):
        suits = [card.suit for card in hand]
        
        # True + True == 2
        # So I'm checking if there's only a single suit in the hand
        suit_check = (Suit.HEARTS in suits) + (Suit.DIAMONDS in suits) + (Suit.CLUBS in suits) + (Suit.SPADES in suits)
        # If it's greater than one it can't be a flush
        return suit_check == 1

    def is_straight(self):
        pass

if __name__ == "__main__":
    print("evaluator")
    k = TexasHandEvaluator()

