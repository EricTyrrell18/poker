#!/usr/bin/env python3
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
        test.gen_high_cards()
        test.gen_pairs()
        test.gen_two_pairs()
        test.gen_three_of_kind()
        test.gen_straights()
        test.gen_flushes()
        test.gen_full_house()
        test.gen_four_of_kind()

    def save_hand_db(self):
        f = open("handDB.pkl", "wb")
        pickle.dump(self.hand_rankings, f)
        f.close()

    def generate_hash(self, combo):
        # Not a Cryptographic hash
        # But it should be a unique identifier
        # Something about prime factorization
       
        # Multiplies all numbers together
        return reduce(lambda x,y: x*y, [c.value for c in combo]) 
    def gen_hand(self, combo):
        hand_hash = self.generate_hash(combo)
        print("{} is {}:{} ".format([c.name for c in combo], self.id, hand_hash))
        self.hand_rankings[hand_hash] = self.id
        self.id += 1
        

    def gen_high_cards(self):
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
        #Go through all the pairs starting at two
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
        for i in range(13):
            three_of_kind = (self.ranks[i],) * 3
            cards_left = list(Rank)
            del cards_left[i]
            for comb in combinations(cards_left,2):
                self.gen_hand(three_of_kind + comb)
    def gen_straights(self):
        # Should only ever be called after gen_high_cards has been called
        for combo in self.straights:
            self.gen_hand(combo)

    def gen_flushes(self):
        # Create empty space for regular flushes to live in 
        # Logic for whether or not it's a flush is left in the evaluator 
        self.id += 1277
    def gen_full_house(self):
        for i in range(13):
            three_of_kind = (self.ranks[i],) * 3

            cards_left = list(Rank)
            del cards_left[i]

            for j in cards_left:
                pair = (j,) * 2
                self.gen_hand(three_of_kind + pair)
    def gen_four_of_kind(self):
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
