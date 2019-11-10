#!/usr/bin/env python3
"""Module pertaining to Poker Players"""
from enum import Enum
import re
class Player():
    """Player base class"""
    def __init__(self, name):
        self.name = name
        self.stack_size = 500
        #Use this to keep track of how much money they have in the current street of action
        self.cur_bet = 0

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
  
    def get_action(self, cur_bet):
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
        elif self.stack_size - cur_bet < 0:
            print("Fold or All in")
        elif cur_bet == 0:
            print("Check or Bet")
        #elif not action_is_open:
        #    print("Fold or Call")
        else:
            print("Fold, call or raise")
        import texas_holdem
        action = input() 
        print(action)
        if action == "Fold":
            bet = 0
        elif action == "Bet":
            print("{} chips".format(str(self.stack_size)))
            bet = int(input("How much do you want to bet?"))
        elif action == "Raise":
            print("{} chips".format(str(self.stack_size)))
            bet = int(input("How much do you want to bet?"))
        elif action == "Call":
            bet = 0
        elif action == "Check":
            bet = 0 
        elif action == "All in":
            bet = self.stack_size
        else: 
            raise ValueError("invalid Action")

        return (action, bet)

    def get_cur_bet(self):
        return self.cur_bet

    def add_to_stack(self, chips):
        self.stack_size += chips

    def win_hand(self, chips):
        self.add_to_stack(chips)

    def subtract_from_stack(self, chips):
        chips = (chips - self.cur_bet)
        if chips > self.stack_size:
            raise ValueError("Not Enough chips, did you mean to go all in instead?")
        self.stack_size -= chips 
        self.cur_bet += chips

    def display_player(self):
        print("name: {}".format(self.name))
        print("chips: {}".format(self.stack_size))
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
        if not bet >= 0:
            raise ValueError
        self.bet = bet
    
