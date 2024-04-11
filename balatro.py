import json

import pandas as pd
import numpy as np


SUITS = ['spades', 'hearts', 'clubs', 'diamonds']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
CHIPS_PER_VALUE = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 7,
    '9': 8,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11}
STRAIGHTS = [
    {'A', '2', '3', '4', '5'},
    {'2', '3', '4', '5', '6'},
    {'3', '4', '5', '6', '7'},
    {'4', '5', '6', '7', '8'},
    {'5', '6', '7', '8', '9'},
    {'6', '7', '8', '9', '10'},
    {'7', '8', '9', '10', 'J'},
    {'8', '9', '10', 'J', 'Q'},
    {'9', '10', 'J', 'Q', 'K'},
    {'10', 'J', 'Q', 'K', 'A'}]

f = open('../data/hand_level_increase.json')
HAND_LEVEL_INCREASE = json.load(f)
f.close()


class Deck():
    def __init__(self):
        self.cards = pd.DataFrame(columns=[
            "value",
            "suit",
            "base_chip_value"
        ])
        self._initialize_deck(SUITS, VALUES)

    def __repr__(self):
        return self.cards.to_markdown()

    def _initialize_deck(self, suits, values):
        for suit in suits:
            for value in values:
                chip_value = CHIPS_PER_VALUE[value]
                self.add_card(value, suit, chip_value)

    def add_card(self, value, suit, base_chip_value):
        new_card = {
            "value": value,
            "suit": suit,
            "base_chip_value": base_chip_value
        }
        self.cards.loc[len(self.cards)] = new_card

    def shuffle(self):
        self.cards = self.cards.sample(frac=1)


class Hand():
    def __init__(self):
        self._empty_df = pd.DataFrame(columns=[
            "value",
            "suit",
            "base_chip_value"
        ])
        self.hand_level = {
            'high_card': 1,
            'pair': 1,
            'three_of_a_kind': 1,
            'four_of_a_kind': 1,
            'five_of_a_kind': 1,
            'two_pair': 1,
            'full_house': 1,
            'flush': 1,
            'straight_flush': 1,
            'straight': 1,
            'flush_house': 1,
            'flush_five': 1
        }
        self.cards = self._empty_df

    def __repr__(self):
        return self.cards.to_markdown()

    def _find_best_n_hand(self, n, feat='value', retrieve_top=1):
        count_list = self.cards[feat].value_counts()

        if (count_list >= n).any():
            elegible_values = count_list[count_list >= n].index
        else:
            return

        elegible = self.cards[self.cards[feat].isin(elegible_values)].sort_values(
            [feat, 'base_chip_value'],
            ascending=[False, False]
        ).groupby(feat).head(n)

        totals = elegible.groupby(feat).base_chip_value.sum()
        best_totals = totals.sort_values(ascending=False).drop_duplicates()

        return elegible[elegible[feat].isin(best_totals[:retrieve_top].index)]

    def draw_from_deck(self, deck, n=7):
        self.cards = pd.concat([self.cards, deck.cards[:n]])
        deck.cards = deck.cards[n:].copy()

    def find_best_high_card(self):
        max_chip_value = self.cards.base_chip_value.max()
        return self.cards[self.cards.base_chip_value == max_chip_value].head(1)

    def find_best_pair(self):
        return self._find_best_n_hand(2)

    def find_best_three_of_a_kind(self):
        return self._find_best_n_hand(3)

    def find_best_four_of_a_kind(self):
        return self._find_best_n_hand(4)

    def find_best_five_of_a_kind(self):
        return self._find_best_n_hand(5)

    def find_best_two_pair(self):
        value_count_list = self.cards.value.value_counts()

        if (value_count_list >= 2).any():
            elegible_pairs = value_count_list[value_count_list >= 2].index
        else:
            return

        if len(elegible_pairs) >= 2:
            elegible = self.cards[self.cards.value.isin(elegible_pairs)].sort_values(
                ['value', 'base_chip_value'],
                ascending=[False, False]
            ).groupby('value').head(2)

            pair_totals = elegible.groupby('value').base_chip_value.sum()
            best_totals = pair_totals.sort_values(ascending=False).drop_duplicates()
            best_two_pair_values = best_totals.head(2).index

            return elegible[elegible.value.isin(best_two_pair_values)]
        else:
            return

    def find_best_full_house(self):
        temp_hand = self.cards.copy()
        best_three = self.find_best_three_of_a_kind()        

        if best_three is not None:
            self.cards.drop(best_three.index, inplace=True)
            best_pair = self.find_best_pair()

            if best_pair is not None:
                self.cards = temp_hand
                return pd.concat([best_pair, best_three])
        else:
            self.cards = temp_hand
            return

    def find_best_flush(self):
        return self._find_best_n_hand(5, feat='suit')

    def find_best_straight(self):
        totals = {}
        hands = {}

        for straight in STRAIGHTS:
            if straight.issubset(set(self.cards.value.values)):
                straight_hand = self.cards[self.cards.value.isin(straight)].copy()
                straight_hand = straight_hand.sort_values(
                    'base_chip_value', ascending=False
                ).groupby('value').head(1)
    
                totals[next(iter(straight))] = straight_hand.base_chip_value.sum()
                hands[next(iter(straight))] = straight_hand

        if len(totals) > 0:
            return hands[sorted(totals.items(), key=lambda x:x[1])[-1][0]]
        else:
            return

    def find_best_straight_flush(self):
        temp_cards = self.cards

        totals = {}
        hands = {}
        for suit in SUITS:
            self.cards = self.cards[self.cards.suit == suit].copy()
            best_straight = self.find_best_straight()

            if best_straight is not None:
                totals[suit] = best_straight.base_chip_value.sum()
                hands[suit] = best_straight

            self.cards = temp_cards

        if len(totals) > 0:
            return hands[sorted(totals.items(), key=lambda x:x[1])[-1][0]]
        else:
            return

    def find_best_flush_house(self):
        temp_cards = self.cards

        totals = {}
        hands = {}
        for suit in SUITS:
            self.cards = self.cards[self.cards.suit == suit].copy()
            best_full_house = self.find_best_full_house()

            if best_full_house is not None:
                totals[suit] = best_full_house.base_chip_value.sum()
                hands[suit] = best_full_house

            self.cards = temp_cards

        if len(totals) > 0:
            return hands[sorted(totals.items(), key=lambda x:x[1])[-1][0]]
        else:
            return

    def find_best_flush_five(self):
        temp_cards = self.cards

        totals = {}
        hands = {}
        for suit in SUITS:
            self.cards = self.cards[self.cards.suit == suit].copy()
            best_five_of_a_kind = self.find_best_five_of_a_kind()

            if best_five_of_a_kind is not None:
                totals[suit] = best_five_of_a_kind.base_chip_value.sum()
                hands[suit] = best_five_of_a_kind

            self.cards = temp_cards

        if len(totals) > 0:
            return hands[sorted(totals.items(), key=lambda x:x[1])[0][0]]
        else:
            return

    def find_best_poker_hand(self):

        hands = {
            'high_card': self.find_best_high_card(),
            'pair': self.find_best_pair(),
            'three_of_a_kind': self.find_best_three_of_a_kind(),
            'four_of_a_kind': self.find_best_four_of_a_kind(),
            'five_of_a_kind': self.find_best_five_of_a_kind(),
            'two_pair': self.find_best_two_pair(),
            'full_house': self.find_best_full_house(),
            'flush': self.find_best_flush(),
            'straight_flush': self.find_best_straight_flush(),
            'straight': self.find_best_straight(),
            'flush_house': self.find_best_flush_house(),
            'flush_five': self.find_best_flush_five()
        }

        totals = {}
        for poker_hand in hands.keys():
            if hands[poker_hand] is not None:
                base = HAND_LEVEL_INCREASE[poker_hand]
                totals[poker_hand] = (
                    (self.hand_level[poker_hand] * int(base['chips']) + hands[poker_hand].base_chip_value.sum())
                    * 
                    (self.hand_level[poker_hand] * int(base['mult']))
                )

        best_poker_hand = sorted(totals.items(), key=lambda x:x[1])[-1][0]

        return best_poker_hand, totals[best_poker_hand]
