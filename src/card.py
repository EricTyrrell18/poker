#!/usr/bin/env python3

from rank import Rank
from suit import Suit

class Card:
    def __init__(self, rank, suit):
        if not suit in Suit:
            raise ValueError("suit value not Suit Enum")
        if not rank in Rank:
            raise ValueError("rank value not in Rank Enum")

        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank.name.lower(), self.suit.name.lower())

    def get_suit(self):     
    	return self.suit
    def get_rank(self):
        return self.rank




if __name__ == "__main__":
    print("card.py tests")

    c1 = Card(Rank.ACE, Suit.HEARTS)
    
    assert c1.suit in Suit and c1.rank in Rank 
   
    print("card.py tests over")
    print(str(c1))
