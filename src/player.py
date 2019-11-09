#!/usr/bin/env python3
"""Module pertaining to Poker Players"""
class Player():
    """Player base class"""
    def __init__(self, name):
        self.name = name

    def get_hand(self):
        return self.hand
    def set_hand(self, hand):
        self.hand = hand
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
   

