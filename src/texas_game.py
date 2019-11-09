#!/usr/bin/env python3
from game import Game
from texas_hand_eval import TexasHandEvaluator
from texas_hand import TexasHoldemHand
from player import Player
from deck import Deck
from itertools import combinations
class TexasHoldemGame(Game):
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
