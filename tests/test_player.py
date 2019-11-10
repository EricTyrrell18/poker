#!/usr/bin/env python3

import sys
sys.path.append("../src")


from player import Player

import unittest

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Jerry")

    def test_subtract_from_stack(self):
        self.player.subtract_from_stack(49)


        self.player.subtract_from_stack(100)
        self.assertEqual(self.player.stack_size, 400)
        self.assertEqual(self.player.cur_bet, 100)

    def test_subtract_too_much_raises_error(self):
        with self.assertRaises(ValueError):
            self.player.subtract_from_stack(501)


if __name__ == "__main__":
    unittest.main()
