#!/usr/bin/env python3

"""
Run this module to create a hand rank dictionary.
Generates the ranks for each possible hand in Texas Hold'em
Note: Despite having space set aside for flushes, this script only looks at the Rank (A,K,Q,7,2) of the cards, and not the suits.
This means That an evaluating function will have to add a magic number of 5863 to flushes.
This'll put all regular flushes in the flush area of the dict, and all straight flushes to the top
"""
import sys
import pickle
from cards import Card, Deck, Rank, Suit
from itertools import islice, combinations
from functools import reduce
class FiveCardGenerator():
    """I saw something like this method online, but I can't be bothered to look it up yet"""

    def __init__(self):
        self.deck = Deck()
        self.id = 1
        self.ranks = list(Rank)
        self.hand_rankings = dict()
        #Empty list of straights so that we can add them in at the right position
        # Starts with 6 high straight so we can easily generate in the gen_high_cards func
        self.straights = [(Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX,)]
    def create_hand_db(self):
        """Add the hands sequentially to the dict"""
        self.gen_high_cards()
        self.gen_pairs()
        self.gen_two_pairs()
        self.gen_three_of_kind()
        self.gen_straights()
        self.gen_flushes()
        self.gen_full_house()
        self.gen_four_of_kind()

    def save_hand_db(self):
        f = open("handDB.pkl", "wb")
        pickle.dump(self.hand_rankings, f)
        f.close()

    def generate_hash(self, combo):
        """
        Generates unique numbers for each possible hand.
        This works because each card is represented by a prime number,
        and n primes multiplied together will give a unique product,
        I think. Don't have a proof, but it seems to work.
        """
        # Multiplies all numbers together
        return reduce(lambda x,y: x*y, [c.value for c in combo]) 

    def gen_hand(self, combo):
        """adds the hand to the dictionary"""
        hand_hash = self.generate_hash(combo)
        print("{} is {}:{} ".format([c.name for c in combo], self.id, hand_hash))
        self.hand_rankings[hand_hash] = self.id
        self.id += 1
        

    def gen_high_cards(self):
        """
        Generates all the highcard hands from 7 high to Ace High.
        6 high hand is just a straight, so it's not included
        Additionally, this will generate all straights greater than 6 high.
        6 High straight is part of the initial self.straights list
        """
        # Start at low end and go all the way to ace highs
        # Grab straights on the way in
        cur_hand = 5
        # 7-Aces 
        for i in range(5,13): 
            possible = islice(Rank,i)
            print(self.ranks[cur_hand])
            for combo in combinations(possible,4):
                combo = combo + (self.ranks[i],)
                if self.is_straight(combo):
                    # We can send this away for now
                    continue
                else:
                    # Add the current number to the combo 
                    self.gen_hand(combo)

    def gen_pairs(self):
        """Generates all pairs"""
        for i in range(13):
            # Create the pair
            pair = (self.ranks[i],) * 2
            # Create the combos of cards left
            # Easier to do than create a deep copy
            cards_left = list(Rank)
            # Remove the paired card from the list
            del cards_left[i]

            for comb in combinations(cards_left,3):
                self.gen_hand(pair+comb)

    def gen_two_pairs(self):
        """Generates all two pairs."""
        for i in range(13):
            first_pair = (self.ranks[i],) * 2
            cards_left = list(Rank)
            print(i)
            del cards_left[i]
            # Only look at pairs below this current pair
            for j in range(i):
                print(j)
                second_pair = (cards_left[j],) * 2
                cards_left_high_card = list(self.ranks)
                del cards_left_high_card[i]
                del cards_left_high_card[j]
                for card in combinations(cards_left_high_card,1):
                    self.gen_hand(first_pair+second_pair+card)

    def gen_three_of_kind(self):
        """Generates all three of a kind."""
        for i in range(13):
            three_of_kind = (self.ranks[i],) * 3
            cards_left = list(Rank)
            del cards_left[i]
            for comb in combinations(cards_left,2):
                self.gen_hand(three_of_kind + comb)
    def gen_straights(self):
        """
        Adds straights to the list of hands.
        Straights should have been generated by gen_high_cards
        """
        for combo in self.straights:
            self.gen_hand(combo)

    def gen_flushes(self):
        """
        Creates an empty space in the dict for flushes to live.
        It doesn't however fill in these spaces, they're just reserved
        An evaluator might get a 9 high hand which is a flush
        The evaluator would find the hand_rank of the hand, 
        and then add the flush offset to get the correct rank
        """
        self.id += 1277
    def gen_full_house(self):
        """Generates Full Houses."""
        for i in range(13):
            three_of_kind = (self.ranks[i],) * 3

            cards_left = list(Rank)
            del cards_left[i]

            for j in cards_left:
                pair = (j,) * 2
                self.gen_hand(three_of_kind + pair)
    def gen_four_of_kind(self):
        """Generates Four of a kinds."""
        for i in range(13):
            # Create the pair
            four_of_kind = (self.ranks[i],) * 4
            # Create the combos of cards left
            # Easier to do than create a deep copy
            cards_left = list(Rank)
            # Remove the paired card from the list
            del cards_left[i]
            # Only space for one more card in hand
            for card in combinations(cards_left, 1):
                self.gen_hand(four_of_kind + card)


    def is_straight(self, combo):
        """
        Determines if a hand is a straight.
        Handles Ace low straight via Ace High Straight
        """
        # Since we know the largest card will always be last
        # We can just calculate membership based on membership
        values = [c.value for c in combo]  
        value_map = [r.value for r in self.ranks]
        high_value = values[-1]
        # Handle ace low straights
        if high_value == Rank.ACE.value:
            if Rank.TWO.value in values and Rank.THREE.value in values and Rank.FOUR.value in values and Rank.FIVE.value in values:
                #Lowest Straight
                self.straights.insert(0,combo)
                return True
        val_index = value_map.index(high_value)
        # Check that the other four cards of the straight are there
        if value_map[val_index - 1] in values and value_map[val_index - 2] in values and value_map[val_index - 3] in values and value_map[val_index - 4] in values:
            print("Adding to straights: {}".format(combo))
            self.straights.append(combo)
            return True
        # Default to not being a straight
        return False
 
if __name__ == "__main__":
    test = FiveCardGenerator()
    test.create_hand_db()
    test.save_hand_db()
