#!/usr/bin/env python3
import enum

class Rank(enum.Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


if __name__ == "__main__":
    print("Starting Rank tests")
    print(enum.__file__)
    assert Rank.TWO.value == 2
    assert Rank.ACE.value == 14
    assert Rank.SEVEN.value == 7
