#!/usr/bin/env python3
"""Module pertaining to Poker Players"""
from enum import Enum
import re
import logging
class Player():
    """Player base class"""
    def __init__(self, name):
        self.name = name
        self.chips = 500
        #Use this to keep track of how much money they have in the current street of action
        self.cur_bet = 0
        self.test = 0
    def __eq__(self, other):
        return self.name == other.name

    def get_hand(self):
        return self.hand
    def set_hand(self, hand):
        self.hand = hand
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
  
    def get_action(self, cur_bet, min_bet):
        """
        Determines what actions the players allowed to make and prompts them.
        Basic scenarios to be aware of include (Big Blind = 2):
        Noone opens preflop before The bigblind:  check or raise
        First player to act with 500 chips: Check or bet
        First player to act with 1 chip: Check or All in
        First player to act with 3 chips: Check, or Bet
        
        For the next few examples theFirst player goes all in for 400 chips,
        Second Player has 800 chips: Fold, call, All in 
        Second Player has 300 chips: fold, All in 
        Second Player has 1800 chips: Fold, Call, Raise

        Scenario: 
        First player bets 200
        Second player goes calls
        Third Player goes all in for 399 chips
        The action isn't reopened because it isn't at least the minimum bet size
        so first player can: Fold, or call
        second player can: Fold, or call
        """
        print("It's your turn {}.".format(self.name))
        print("What will you do?")
        if self.cur_bet == cur_bet:
            #Should only be called when it is preflop and the action gets back to the big blind and no one's raised
            print("Check or Raise")
        elif self.chips - cur_bet < 0:
            print("Fold or All in")
        elif cur_bet == 0:
            print("Check or Bet")
        #elif not action_is_open:
        #    print("Fold or Call")
        else:
            print("Fold, call or raise")
        
        valid_action = False
        action = None

        while not valid_action:
            try:
                action = PlayerAction(self.get_input_action(), 0)
                if action.get_action() == PlayerActionEnum.ALL_IN:
                    action.set_bet(self.chips)
                elif action.get_action() == PlayerActionEnum.BET:
                    print("action is bet")
                    bet = self.get_input_bet()
                    action.set_bet(bet)
                    print("bet = {}".format(action.get_bet()))
                    if action.get_bet() > self.chips:
                        raise ValueError("Don't have enough chips")
                    if action.get_bet() < min_bet:
                        raise ValueError("Bet not large enough")
                elif action.get_action() == PlayerActionEnum.CALL:
                    action.set_bet(cur_bet)
                elif action.get_action() == PlayerActionEnum.FOLD:
                    pass
                else:
                    print("What is this?")
                valid_action = True
            except ValueError:
                continue
        self.make_bet(action.get_bet()) 

        return action

    def get_cur_bet(self):
        return self.cur_bet
    def get_chips(self):
        return self.chips

    def add_to_stack(self, chips):
        self.chips += chips

    def win_hand(self, chips):
        self.add_to_stack(chips)

    def get_input_bet(self):
        print("{} chips".format(str(self.chips)))
        bet = int(input("How much do you want to bet?"))
        self.test = bet
        return bet

    def get_input_action(self):
        action = input("What action will you take?")
        return action

    def make_bet(self, chips):
        """Subtract the bet from our chips and make a note of how much we've bet"""
        self.chips -= (chips - self.cur_bet)
        self.cur_bet = chips

    def subtract_from_stack(self, chips):
        chips = (chips - self.cur_bet)
        if chips > self.chips:
            raise ValueError("Not Enough chips, did you mean to go all in instead?")
        self.chips -= chips 
        self.cur_bet += chips

    def display_player(self):
        print("name: {}".format(self.name))
        print("chips: {}".format(self.chips))
        print("cur_bet: {}".format(self.cur_bet))



class PlayerActionEnum(Enum):
    CHECK = 0
    CALL = 1
    BET = 2
    RAISE = 3
    ALL_IN = 4
    FOLD = 5

    @staticmethod        
    def grok_action(action):
        """Determines which action a string is by using Regex"""
        check_regex = r"^[Cc]heck$"
        call_regex = r"^[Cc]all$"
        bet_regex = r"^[Bb]et$"
        raise_regex = r"^[Rr]aise$"
        all_in_regex = r"^[Aa]ll ?[Ii]n$"
        fold_regex = r"^[Ff]old"
        if re.search(check_regex, action):
            return PlayerActionEnum.CHECK
        elif re.search(call_regex, action):
            return PlayerActionEnum.CALL
        elif re.search(bet_regex, action):
            return PlayerActionEnum.BET
        elif re.search(raise_regex, action):
            return PlayerActionEnum.RAISE
        elif re.search(all_in_regex, action):
            return PlayerActionEnum.ALL_IN
        elif re.search(fold_regex, action):
            return PlayerActionEnum.FOLD
        else:
            raise ValueError("Please retype your action")


class PlayerAction():
    def __init__(self, action, bet):
        self.set_action(action)
        self.set_bet(bet)

    def get_action(self):
        return self.action

    def get_bet(self):
        return self.bet

    def set_action(self, action):
        self.action = PlayerActionEnum.grok_action(action)

    def set_bet(self, bet):
        print(bet)
        if bet < 0:
            raise ValueError("Bet has to be bigger than 0")
        self.bet = bet
    
