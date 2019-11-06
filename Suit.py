#!/usr/bin/env python3
import enum
class Suit(enum.Enum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4

if __name__ == "__main__":
    print("Suit Test")
    assert Suit.HEARTS.value == 1
    assert Suit.DIAMONDS.value == 2
    assert Suit.SPADES.value == 3
    assert Suit.CLUBS.value == 4
    print("Enum Tests Finished")
