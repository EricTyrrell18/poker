#!/usr/bin/env python3
from game import Game
from texas_hand import TexasHoldemHand
from player import Player
from deck import Deck
class TexasHoldemGame(Game):
    def start_hand(self):
        self.deck.shuffle()
        self.deal_cards()
    
    def flop(self):
        self.flop = [1,2,3]

    def turn(self):
        self.turn = [1]
   
    def river(self):
        self.river = [1]

    def deal_hole_cards(self):
        for player in self.players:
            hand = TexasHoldemHand(self.deck.deal_card(),self.deck.deal_card())
            player.set_hand(hand)

    def display_players(self):
        for player in self.players:
            print("{}: {}".format(player.name, player.get_hand()))
    
if __name__ == "__main__":
    print("Starting game")
    player1 = Player("Rick")
    player2 = Player("Morty")
    game = TexasHoldemGame(Deck(), player1, player2)
    game.start_hand()
    game.display_players()
