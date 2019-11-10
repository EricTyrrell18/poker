#!/usr/bin/env python3

import sys
sys.path.append("../src/")

import unittest
from player import PlayerActionEnum, PlayerAction

class TestPlayerActionEnum(unittest.TestCase):
    def test_grok_action(self):
        self.assertEqual(PlayerActionEnum.grok_action("check"), PlayerActionEnum.CHECK)
        self.assertEqual(PlayerActionEnum.grok_action("call"), PlayerActionEnum.CALL)
        self.assertEqual(PlayerActionEnum.grok_action("bet"), PlayerActionEnum.BET)
        self.assertEqual(PlayerActionEnum.grok_action("raise"), PlayerActionEnum.RAISE)
        self.assertEqual(PlayerActionEnum.grok_action("all in"), PlayerActionEnum.ALL_IN)
        with self.assertRaises(ValueError):
            PlayerActionEnum.grok_action("Not an action")

class TestPlayerAction(unittest.TestCase):
    def test_init_action(self):
        action = PlayerAction("Check", 10)
        self.assertEqual(action.get_action(), PlayerActionEnum.CHECK)
        action = PlayerAction("Call", 10)
        self.assertEqual(action.get_action(), PlayerActionEnum.CALL)
        action = PlayerAction("Bet", 10)
        self.assertEqual(action.get_action(), PlayerActionEnum.BET)
        action = PlayerAction("Raise", 10)
        self.assertEqual(action.get_action(), PlayerActionEnum.RAISE)
        action = PlayerAction("All In", 10)
        self.assertEqual(action.get_action(), PlayerActionEnum.ALL_IN)
        with self.assertRaises(ValueError):
            action = PlayerAction("Not an Action", 10)
    
    def test_init_bet(self):
        action = PlayerAction("Check", 100)
        self.assertEqual(action.get_bet(), 100)
        action = PlayerAction("Call", 1000)
        self.assertEqual(action.get_bet(), 1000)
        with self.assertRaises(ValueError):
            action = PlayerAction("Bet", -1)
        

if __name__ == "__main__":
    unittest.main()
