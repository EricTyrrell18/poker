#!/usr/bin/env python3
"""Module for Texas Hold'em."""
from cards import Card, Suit, Deck

from functools import reduce
from player import Player, PlayerAction, PlayerActionEnum
from enum import Enum
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

class TexasHoldemState():
    """Class responsible for maintaining the state of the hand."""
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.board = []
        self.button = 0
        
        self.big_blind = 2
        self.small_blind = 1
        self.pot = self.small_blind + self.big_blind
        self.cur_bet = 2
        # Used to determine when to move to the next street
        # If play goes around to the last aggressor, Move to next street
        # Special note may be preflop Big blind
        self.last_aggressor = Player("Not A Person")
        self.counter = 0
        # check/bet/raise/fold = 0/1/2/3
        self.last_action = 0
        self.minimum_bet_size = 2
        self.is_anti = False
        self.anti = 0

    def flop(self):
        """Deals three cards on the flop"""
        for i in range(3):
           self.board.append(self.deck.deal_card())
        self.last_action = 0
        self.cur_bet = 0
        self.clean_state()

    def turn(self):
        """Deals one card on the turn"""
        self.board.append(self.deck.deal_card())
        self.clean_state()

    def river(self):
        """Deals one card on the river"""
        self.board.append(self.deck.deal_card())
        self.clean_state()

    def reinit(self, num_of_players):
        """Reinitialize state for the beginning of a new hand"""
        self.board = []
        self.deck.shuffle()
        self.button = (self.button + 1) % num_of_players
        self.pot = self.big_blind + self.small_blind
        self.minimum_bet_size = self.big_blind
        self.cur_bet = self.big_blind
        self.last_aggressor = Player("Not a Player")
        self.counter = 0

    def clean_state(self):
        """Cleans up the state after action closes on a street"""
        self.last_action = 0
        self.cur_bet = 0
        self.minimum_bet_size = 0
        self.last_aggressor = Player("Not a PLayer")
        self.counter = 0

    def display_board(self):
        """Print the cards on the table."""
        print([str(c) for c in self.board])

    def display_state(self):
        print("current pot size is {}".format(self.pot))
        print("current bet is {}".format(self.cur_bet))
        print("current minimum bet is {}".format(self.minimum_bet_size))
        self.display_board()

class EOHError(EOFError):
    """Error used to signal that a hand's done"""
    def __init__(self,arg):
        self.strerror=arg
        self.args = {arg}

class TexasHoldemGame():
    """Game Implementations of Texas Hold'em."""

    def __init__(self, *players):
        """Crete the Evaluator, Deck, and Players."""
        self.evaluator = TexasHandEvaluator()
        self.players = list(players)
        self.cur_players = list(players)
        self.state = TexasHoldemState()
        self.small_blind = 0
        self.big_blind = 0

    def start_hand(self):
        """Clear the board, shuffle the deck, and begin the hand"""
        self.state.reinit(len(self.players))
        self.deal_hole_cards() 
        
        #Set up the blinds
        self.small_blind = (self.state.button + 1) % len(self.players)
        self.players[self.small_blind].make_bet(1)

        self.big_blind = (self.state.button + 2) % len(self.players)  
        self.players[self.big_blind].make_bet(2)

        self.play_hand()
        

    def play_hand(self):
        try:
            self.preflop_actions()
            self.flop_actions()
            self.turn_actions()
            self.river_actions()
            self.showdown()
            self.end_hand()
        except EOHError:
            self.end_hand()

    def get_player_actions(self):
        """
        Go through all the player actions.
        Check/Bet/Raise/Fold
        """
        #TODO:Should start at small blind, but this works for now
        #for player in self.cur_players:
        #    player.display_player()
        #    action, bet = player.get_action(self.state.cur_bet) 
        #   
        #    self.perform_player_action(player, action, bet)
        
        cur_player_index = self.small_blind
        # When it's the beginning of a hand, action begins with the player after the big blind
        if self.state.board == []:
            cur_player_index = (self.big_blind + 1) % len(self.cur_players)
        else:
            self.clean_players()
        # Used to check if the players checked, or folded, around
        initial_player_count = len(self.cur_players)

        # If there's only one player left end the hand
        while len(self.cur_players) > 1:
            player = self.cur_players[cur_player_index]
            # Check if action should continue
            if player == self.state.last_aggressor or self.state.counter == initial_player_count:
                break
            # If there's a bet, it resets the counter
            print("pot: {} chips".format(self.state.pot))
            player.display_player()

            action = player.get_action(self.state.cur_bet, self.state.minimum_bet_size) 
           
            self.perform_player_action(player, action)

            cur_player_index = (cur_player_index + 1) % len(self.cur_players)

            self.state.counter += 1

        if len(self.cur_players) == 1:
            raise EOHError("End of Hand")
        #Reset players for the next street
        for player in self.cur_players:
            player.cur_bet = 0

    def preflop_actions(self):
        print("Preflop")
        self.state.display_state()
        self.get_player_actions()

    def flop_actions(self):
        print("Flop")
        self.state.flop()
        self.state.display_state()
        self.get_player_actions()
        
    def clean_players(self):
        for player in self.players:
            player.cur_bet = 0
            player.prev_bet = 0

    def turn_actions(self):
        print("turn")
        self.state.turn()
        self.state.display_state()
        self.get_player_actions()

    def river_actions(self):
        print("river")
        self.state.river()
        self.state.display_state()
        self.get_player_actions()

    def deal_hole_cards(self):
        """Deals cards to every player."""
        for player in self.players:
            #TODO: create a function to deal texas holdem hands in state
            hand = TexasHoldemHand(self.state.deck.deal_card(),self.state.deck.deal_card())
            player.set_hand(hand)



    def perform_player_action(self, player, action):
        """
        Handle actions which will affect the state.
        May throw value errors if a bet size is too small.
        Seems like raising and betting have the same affect,
        but I'm going to keep them separate just in case it needs to be changed.
        """
        if action.get_action() == PlayerActionEnum.CHECK:
            self.handle_check(player)
        elif action.get_action() == PlayerActionEnum.CALL:
            self.handle_call(player, action.get_bet())
        elif action.get_action() == PlayerActionEnum.BET:
            self.handle_bet(player, action.get_bet())
        elif action.get_action() == PlayerActionEnum.RAISE:
            self.handle_bet(player, action.get_bet())
        elif action.get_action() == PlayerActionEnum.ALL_IN:
            self.handle_bet(player, action.get_bet())
        elif action.get_action() == PlayerActionEnum.FOLD:
            self.handle_fold(player)
        else:
            raise ValueError("Invalid action: {}")

    def handle_check(self, player):
        """
        Handles the check action.
        If the last action performed was, checking isn't allowed. 
        Raise an error.
        """
        print("Player's cur_ber: {}".format(player.get_cur_bet()))
        print("state cur_bet: {}".format(self.state.cur_bet))
        print( self.state.cur_bet == player.get_cur_bet())
        if self.state.cur_bet != player.get_cur_bet():
            #Unless you're the bigblind and it checks around to you
            raise ValueError("You cannot check when there's been a bet")

    def handle_call(self, player, bet):
        """
        Handles the Call action.
        There has to be a current bet,
        otherwise raises a ValueError
        """
        if self.state.cur_bet == 0:
            raise ValueError("You can't call nothing")
        #A player might have been raised and already have chips in the pot
        print(self.state.cur_bet - player.prev_bet)
        self.state.pot += self.state.cur_bet - player.prev_bet
       
    def handle_bet(self, player, bet):
        """
        Handles a bets effect on the board state.
        Raises an error dependent on betsize
        """
        if (bet - self.state.cur_bet) < self.state.minimum_bet_size:
            raise ValueError("Bet is smaller than minimum bet size.")
        # Example: min bet starts at 2 preflop. I open to 6. min bet size should be 4
        # I get reraised to 10. Min bet size should still be 4. 10 - 6 = 4
        print("Bet: {}".format(bet))
        print("Prev bet: {}".format(player.prev_bet))
        self.state.pot += bet - player.prev_bet
        self.state.cur_bet = bet 
        self.state.minimum_bet_size = (bet - self.state.minimum_bet_size)
        self.state.last_aggressor = player 
        self.state.counter = 0

    def handle_raise(self, player, action):
        """
        Same as handle_bet.
        Blank for now, use handle_bet instead
        """
        pass

    def handle_fold(self, player):
        """
        Handles the fold action
        Ask if they really want to fold when there's no reason to
        """
        if self.state.cur_bet == 0:
            raise ValueError("You know you don't have to fold right?")
        self.cur_players.remove(player)
        
    def handle_all_in(self, player, bet):
        """
        Handles all in bets
        Sometimes a player will have less than the minimum bet size, 
        but they still want to bet/raise. Handle bet will throw an error
        so this is needed for when it's the rest of a players stack
        This shouldn't reopen action, and should only be used when
        the player has less than min bet size.
        """
        self.state.last_aggressor = player 
        self.state.pot += bet 
        self.state.cur_bet = bet

    def showdown(self):
        """
        Determines who won the hand.
        Currently, has to go through every 5 card combination to determine the winner.
        This could be improved by creating a seven card dict by leveraging the existing 5 card dict.
        """
        # Pick the winner
        best_hand = -1
        winner_name = "Wrong"
        winner = None
        for player in self.players:
            # combine the hand with the board
            full_hand = self.state.board + player.get_hand().get_hole_cards()
            player_best = -1
            # Convert to 5 card hands and get the best val
            for combo in combinations(full_hand, 5):
                rank = self.evaluator.evaluate_hand(combo)
                if rank > player_best:
                    player_best = rank
                    if rank > best_hand:
                        best_hand = rank
                        winner_name = player.get_name()
                        winner = player
        self.state.display_state()
        print(player.get_hand())
        print(player.name + ": {}".format(player_best))
        print(best_hand)
        print(winner_name)
        return winner
    
    def end_hand(self):
        """Cleanup required after the hand's over"""
        winner = None
        if len(self.cur_players) == 1:
            winner = self.cur_players[0]
        else:
            # Doesn't currently handle ties, or side pots
            winner = self.showdown()
        print("{} has won the hand".format(winner.get_name()))
        print("{} has won {} chips".format(winner.get_name(), self.state.pot))
        winner.win_hand(self.state.pot)

    def display_players(self):
        """Print information about the players"""
        for player in self.players:
            print("{}: {}".format(player.name, player.get_hand()))
   

if __name__ == "__main__":
    print("Starting game")
    player1 = Player("Rick")
    player2 = Player("Morty")
    game = TexasHoldemGame(player1, player2)
    game.start_hand()
