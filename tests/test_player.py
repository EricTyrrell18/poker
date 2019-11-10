#!/usr/bin/env python3

import sys
sys.path.append("../src")


from player import Player, PlayerActionEnum

import unittest
from unittest.mock import MagicMock
import unittest.mock
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Jerry")
    
    def test_make_bet(self):
        self.player.make_bet(200)
        self.assertEqual(self.player.get_chips(), 300)
    
    def test_get_action_bet(self):
        self.player.get_input_action = MagicMock(return_value = "Bet")
        self.player.get_input_bet = MagicMock(return_value = 200)
        action = self.player.get_action(0, 0)
        self.assertEqual(action.get_action(), PlayerActionEnum.BET )

    def test_get_action_bet_200(self):
        self.player.get_input_action = MagicMock(return_value = "Bet")
        self.player.get_input_bet = MagicMock(return_value = 200)

        
        action = self.player.get_action(0,0)
        
        self.assertEqual(action.get_bet(), 200)
        self.assertEqual(self.player.chips, 300)
 

    def test_get_action_check(self):
        self.player.get_input_action = MagicMock(return_value = "Check")
        action = self.player.get_action(0,0)

        self.assertEqual(action.get_action(), PlayerActionEnum.CHECK)

    def test_get_action_call_no_money_committed(self):
        self.player.get_input_action = MagicMock(return_value = "Call")
        action = self.player.get_action(200,0)
        self.assertEqual(action.get_action(), PlayerActionEnum.CALL)
        self.assertEqual(self.player.get_chips(), 300)

    def test_get_action_call_200_chips_committed(self):
        self.player.get_input_action = MagicMock(return_value = "Call")
        self.player.cur_bet = 100
        action = self.player.get_action(200,0)

        #Already committed 100, so only 100 more to call 
        self.assertEqual(self.player.get_chips(), 400)

    def test_get_action_fold(self):
        self.player.get_input_action = MagicMock(return_value = "Fold")
        action = self.player.get_action(4,0)
        self.assertEqual(action.get_action(), PlayerActionEnum.FOLD)

    def test_get_action_all_in(self):
        self.player.get_input_action = MagicMock(return_value = "All In")

        action = self.player.get_action(0,0)

        self.assertEqual(action.get_action(), PlayerActionEnum.ALL_IN)
        self.assertEqual(action.get_bet(), 500)
        self.assertEqual(self.player.get_chips(), 0)



        



if __name__ == "__main__":
    unittest.main()
