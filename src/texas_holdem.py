#!/usr/bin/env python3
from cards import Card, Suit, Deck

from functools import reduce
from player import Player
import sys
import pickle

from itertools import combinations

class TexasHoldemHand():
    def __init__(self, hole_card1, hole_card2):
        """2 cards"""

        self.hole_card1 = hole_card1
        self.hole_card2 = hole_card2
        
    def __str__(self):
        return "{}, {}".format(str(self.hole_card1), str(self.hole_card2))

    def get_hole_cards(self):
        return [self.hole_card1, self.hole_card2]

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

#!/usr/bin/env python3
class TexasHoldemGame():
    def __init__(self, *players):
        self.evaluator = TexasHandEvaluator()
        self.deck = Deck()
        self.players = players

    def start_hand(self):
        self.board = []
        self.deck.shuffle()
        self.deal_hole_cards()
    
    def deal_hole_cards(self):
        for player in self.players:
            hand = TexasHoldemHand(self.deck.deal_card(),self.deck.deal_card())
            player.set_hand(hand)

    def flop(self):
        for i in range(3):
           self.board.append(self.deck.deal_card())

    def turn(self):
        self.board.append(self.deck.deal_card())
   
    def river(self):
        self.board.append(self.deck.deal_card())

    def showdown(self):
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
        for player in self.players:
            print("{}: {}".format(player.name, player.get_hand()))
   
    def display_board(self):
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
