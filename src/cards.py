#!/usr/bin/env python3
import enum
from itertools import product
from random import shuffle
class Rank(enum.Enum):
    """Prime Values for looking up hand values"""
    TWO = 2
    THREE = 3
    FOUR = 5
    FIVE = 7
    SIX = 11
    SEVEN = 13
    EIGHT = 17
    NINE = 19
    TEN = 23
    JACK = 29
    QUEEN = 31
    KING = 37
    ACE = 41


class Suit(enum.Enum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4


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


class Deck():
    def __init__(self):
        """
        52 Cards in a deck. 
        No Jokers.
        """
        # Look at fill_deck to see how this was generated
        self.deck = [Card(Rank.TWO, Suit.HEARTS), Card(Rank.TWO, Suit.DIAMONDS), Card(Rank.TWO, Suit.SPADES), Card(Rank.TWO, Suit.CLUBS), Card(Rank.THREE, Suit.HEARTS), Card(Rank.THREE, Suit.DIAMONDS), Card(Rank.THREE, Suit.SPADES), Card(Rank.THREE, Suit.CLUBS), Card(Rank.FOUR, Suit.HEARTS), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.SPADES), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.FIVE, Suit.HEARTS), Card(Rank.FIVE, Suit.DIAMONDS), Card(Rank.FIVE, Suit.SPADES), Card(Rank.FIVE, Suit.CLUBS), Card(Rank.SIX, Suit.HEARTS), Card(Rank.SIX, Suit.DIAMONDS), Card(Rank.SIX, Suit.SPADES), Card(Rank.SIX, Suit.CLUBS), Card(Rank.SEVEN, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS), Card(Rank.SEVEN, Suit.SPADES), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.EIGHT, Suit.HEARTS), Card(Rank.EIGHT, Suit.DIAMONDS), Card(Rank.EIGHT, Suit.SPADES), Card(Rank.EIGHT, Suit.CLUBS), Card(Rank.NINE, Suit.HEARTS), Card(Rank.NINE, Suit.DIAMONDS), Card(Rank.NINE, Suit.SPADES), Card(Rank.NINE, Suit.CLUBS), Card(Rank.TEN, Suit.HEARTS), Card(Rank.TEN, Suit.DIAMONDS), Card(Rank.TEN, Suit.SPADES), Card(Rank.TEN, Suit.CLUBS), Card(Rank.JACK, Suit.HEARTS), Card(Rank.JACK, Suit.DIAMONDS), Card(Rank.JACK, Suit.SPADES), Card(Rank.JACK, Suit.CLUBS), Card(Rank.QUEEN, Suit.HEARTS), Card(Rank.QUEEN, Suit.DIAMONDS), Card(Rank.QUEEN, Suit.SPADES), Card(Rank.QUEEN, Suit.CLUBS), Card(Rank.KING, Suit.HEARTS), Card(Rank.KING, Suit.DIAMONDS), Card(Rank.KING, Suit.SPADES), Card(Rank.KING, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.ACE, Suit.DIAMONDS), Card(Rank.ACE, Suit.SPADES), Card(Rank.ACE, Suit.CLUBS)]
        # Used for keeping track of cards already dealth
        # Allows the same deck to be reused instead of playing with a copy
        self.dealt_cards = []  
  
    def fill_deck(self):
        # Generate all possible cards
        for rank, suit in product(Rank,Suit):
            # Add the cards to the deck
            self.deck.append(Card(rank,suit))

        # Unroll loop
        # cards = product(Rank, Suit)
        # for card in cards:
        #     print('Card({}, {}),'.format(card[0],card[1])
        # Copy into file
        # in vim
        # :%s/\n//g
        # :%s/,C/, C/g
        # remove trailing ,


    def shuffle(self):
        """Only Call at the beginning of a hand"""
        # Add dealt cards back into deck
        self.deck = self.deck + self.dealt_cards
        self.dealt_cards = []
        shuffle(self.deck)
   
    def deal_card(self):
        # save the card for reshuffling later
        if not len(self.deck) >= 1:
            raise IndexError("No Cards Left To Deal")
        self.dealt_cards.append(self.deck[-1])                
        return self.deck.pop()

