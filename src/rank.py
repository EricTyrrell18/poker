#!/usr/bin/env python3
import enum

class Rank(enum.Enum):
    """Prime Values for looking up hand values"""
    TWO = 2
    THREE = 3
    FOUR = 5
    FIVE = 7
    SIX = 11
    SEVEN = 13
    EIGHT = 17
    NINE = 19
    TEN = 23
    JACK = 29
    QUEEN = 31
    KING = 37
    ACE = 41


if __name__ == "__main__":
    print("Starting Rank tests")
