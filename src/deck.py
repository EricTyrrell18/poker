#!/usr/bin/env python3

from card import Card
from rank import Rank
from suit import Suit
from itertools import product
from random import shuffle
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
   
if __name__ == "__main__":
    # Test creating deck
    deck = Deck()
    assert len(deck.deck) == 52
    # Check dealing cards
    c1 = deck.deal_card()
    assert c1.get_suit() == Suit.CLUBS and c1.get_rank() == Rank.ACE
    assert len(deck.dealt_cards) == 1
    assert len(deck.deck) == 51
    # Shuffle chekc
    deck.shuffle()
    assert len(deck.dealt_cards) == 0
    assert len(deck.deck) == 52
    # Deck with only one card
    deck.deck = [Card(Rank.TWO, Suit.HEARTS)]
    deck.deal_card()
    assert len(deck.deck) == 0
    assert len(deck.dealt_cards) == 1
    
    # There's probably a better way
    # Make sure it can't be overdealt
    try:
        deck.deal_card()
        raise AssertionError("Deck Can be overdealt")
    except IndexError:
        pass



