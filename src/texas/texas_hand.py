#!/usr/bin/env python3

from card import Card

class TexasHoldemHand():
    def __init__(self, hole_card1, hole_card2):
        """2 cards"""

        self.hole_card1 = hole_card1
        self.hole_card2 = hole_card2
        
    def __str__(self):
        return "{}, {}".format(str(self.hole_card1), str(self.hole_card2))


