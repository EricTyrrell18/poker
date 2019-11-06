#!/usr/bin/env python3

from Card import Card
from Rank import Rank
from Suit import Suit
from itertools import product
class Deck():
    def __init__(self):
        """
        52 Cards in a deck. 
        No Jokers.
        """
        self.deck = []
        self.fill_deck()
        

    def fill_deck(self):
        # Generate all possible cards
        # TODO: Determine if product's overkill here
        # Possibly hard code it?
        for rank, suit in product(Rank,Suit):
            # Add the cards to the deck
            self.deck.append(Card(rank,suit))
            
    def shuffle_deck(self):
        pass
   
    def deal_card(self):
        pass
   
if __name__ == "__main__":
    deck = Deck()
    assert len(deck.deck) == 52
