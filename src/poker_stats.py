#!/usr/bin/env python3

from cards import Deck, Rank, Suit

class DeckStatistics():
    def __init__(self):
        self.suits_dict = self.create_suits_dict()
        self.ranks_dict = self.create_ranks_dict()

    def create_suits_dict(self):
        return  { suit: 13 for suit in Suit }

    def create_ranks_dict(self):
        return { rank: 4 for rank in Rank } 

    def suit_count(self, SUIT):
        return self.suits_dict.get(SUIT)
    
    def rank_count(self, RANK):
        return self.ranks_dict.get(RANK)


class PokerStatistics:
    def __init__(self):
        self.deck = Deck()

    def odds_of_specific_card(card):
        return 1/52

    def odds_of_specific_rank(card):
        return 1/13

    def odds_of_specific_suit(card):
        return 1/4

