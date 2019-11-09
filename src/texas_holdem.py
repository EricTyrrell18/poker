#!/usr/bin/env python3
"""Module for Texas Hold'em."""
from cards import Card, Suit, Deck

from functools import reduce
from player import Player
import sys
import pickle

from itertools import combinations

class TexasHoldemHand():
    """Two card Texas Hold'em hand."""
    def __init__(self, hole_card1, hole_card2):
        """2 cards"""

        self.hole_card1 = hole_card1
        self.hole_card2 = hole_card2
        
    def __str__(self):
        return "{}, {}".format(str(self.hole_card1), str(self.hole_card2))

    def get_hole_cards(self):
        return [self.hole_card1, self.hole_card2]

class TexasHandEvaluator():
    """
    Evaluator for Texas Hold'em Hands.
    Uses a database created by create_hands_dict.py.
    """
    def __init__(self):
        """loads the dict"""
        self.load_hand_db()
        #print(self.hand_rankings)
    def load_hand_db(self):
        """Funciton that actually opens the file"""
        f = open("handDB.pkl", "rb")
        self.hand_rankings = pickle.load(f)
        f.close()
    
    def hash_hand(self, hand):
        """
        Helper function to get a unique hash from a hand.
        Works because of prime numbers as the card values
        """
        return reduce(lambda x,y: x*y, [card.rank.value for card in hand] )

    def evaluate_hand(self, hand):
        """
        Evaluates the rank of the hand.
        Gets the rank of the hand from the loaded dict
        If it sees a flush, it adds an offset to move the flush to the right spot.
        """
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
        """
        Checks if the hand's a flush.
        since True + True == 2 
        and True + False = 1
        We can easily check how many suits there are in a hand
        """
        #TODO: Is this actually efficient?
        suits = [card.suit for card in hand]
        
        # True + True == 2
        # So I'm checking if there's only a single suit in the hand
        suit_check = (Suit.HEARTS in suits) + (Suit.DIAMONDS in suits) + (Suit.CLUBS in suits) + (Suit.SPADES in suits)
        # If it's greater than one it can't be a flush
        return suit_check == 1



class TexasHoldemGame():
    """Game Implementations of Texas Hold'em."""

    def __init__(self, *players):
        """Crete the Evaluator, Deck, and Players."""
        self.evaluator = TexasHandEvaluator()
        self.deck = Deck()
        self.players = players

    def start_hand(self):
        """Clear the board, shuffle the deck, and deal the cards."""
        self.board = []
        self.deck.shuffle()
        self.deal_hole_cards()
    
    def deal_hole_cards(self):
        """Deals cards to every player."""
        for player in self.players:
            hand = TexasHoldemHand(self.deck.deal_card(),self.deck.deal_card())
            player.set_hand(hand)

    def flop(self):
        """Deals three cards on the flop"""
        for i in range(3):
           self.board.append(self.deck.deal_card())

    def turn(self):
        """Deals one card on the turn"""
        self.board.append(self.deck.deal_card())
   
    def river(self):
        """Deals one card on the river"""
        self.board.append(self.deck.deal_card())

    def showdown(self):
        """
        Determines who won the hand.
        Currently, has to go through every 5 card combination to determine the winner.
        This could be improved by creating a seven card dict by leveraging the existing 5 card dict.
        """
        # Pick the winner
        best_hand = -1
        winner_name = "Wrong"
        for player in self.players:
            # combine the hand with the board
            full_hand = self.board + player.get_hand().get_hole_cards()
            player_best = -1
            # Convert to 5 card hands and get the best val
            for combo in combinations(full_hand, 5):
                rank = self.evaluator.evaluate_hand(combo)
                if rank > player_best:
                    player_best = rank
                    if rank > best_hand:
                        best_hand = rank
                        winner_name = player.get_name()
            print(player.name + ": {}".format(player_best))
        print(best_hand)
        print(winner_name)

    def display_players(self):
        """Print information about the players"""
        for player in self.players:
            print("{}: {}".format(player.name, player.get_hand()))
   
    def display_board(self):
        """Print the cards on the table."""
        print([str(c) for c in self.board])

if __name__ == "__main__":
    print("Starting game")
    player1 = Player("Rick")
    player2 = Player("Morty")
    game = TexasHoldemGame(player1, player2)
    game.start_hand()
    game.display_players()
    game.flop()
    game.turn()
    game.river()
    game.showdown()
    game.display_board()
