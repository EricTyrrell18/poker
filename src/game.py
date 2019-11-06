#!/usr/bin/env python3

class Game():
    def __init__(self, deck, *players):
        self.deck = deck
        self.players = players

    
    def start_hand(self):
        pass             

    def end_hand(self):
        self.deck.shuffle()


    
