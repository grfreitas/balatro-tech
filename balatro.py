import random
from operator import attrgetter, itemgetter

import pandas as pd


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
    'A': 11,
}


class Card:
    def __init__(self, suit, value):
        if suit in SUITS and value in VALUES:
            self.suit = suit
            self.value = value
            self._set_chip_value()
        else:
            raise TypeError("Suit and/or Value not acceptable.")

        self.is_foiled = False
        self.is_stamped = False
        self.is_modified = False

        self.foil_type = None
        self.stamp_type = None
        self.modification_type = None

    def __repr__(self):
        return f'Card({self.value} of {self.suit.title()})'

    def _set_chip_value(self):
        self.chip_value = CHIPS_PER_VALUE[self.value]


class Deck():
    def __init__(self):
        self.cards = []
        self._initialize_deck(SUITS, VALUES)

    def _initialize_deck(self, suits, values):
        for suit in suits:
            for value in values:
                card = Card(suit, value)
                self.add_card(card)

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)


class Hand():
    def __init__(self):
        self.cards = []
        self.chip_values = list(map(attrgetter("chip_value"), self.cards))
        self.value_occurrence_list = enumerate([
            list(map(lambda m: m.value, hand.cards)).count(value) for value in VALUES
        ])

    def __repr__(self):
        return f'{self.cards}'

    def add_cards(self, cards):
        self.cards.append(cards)

    def draw_from_deck(self, deck, n=7):
        self.cards = deck.cards[:n]
        deck.cards = deck.cards[n:]

    def find_best_high_card_hand(self):
        max_idxs = [
            idx for idx, chip_value in enumerate(self.chip_values) if chip_value == max(self.chip_values)
        ]
        return itemgetter(*max_idxs)(self.cards)

    def find_best_pair_hand(self):
        pass

    def find_best_pair_hand(self):
        pass

    def find_best_two_pair_hand(self):
        pass

    def find_best_flush_hand(self):
        pass

    def find_best_three_of_a_kind_hand(self):
        pass

    def find_best_full_house_hand(self):
        pass

    def find_best_straight_hand(self):
        pass

    def find_best_four_of_a_kind_hand(self):
        pass

    def find_best_straight_flush_hand(self):
        pass

    def find_best_five_of_a_kind_hand(self):
        pass

    def find_best_flush_house_hand(self):
        pass

    def find_best_flush_five_hand(self):
        pass

    def find_best_poker_hand(self):
        pass
    