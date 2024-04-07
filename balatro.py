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
        self.cards = self._empty_df

    def __repr__(self):
        return self.cards.to_markdown()

    def _find_best_n_hand(self, n):
        value_count_list = self.cards.value.value_counts()

        if (value_count_list >= n).any():
            pair_chips = []
            elegible_values = value_count_list[value_count_list >= n].index
        else:
            return

        elegible = self.cards[self.cards.value.isin(elegible_values)].sort_values(
            ['value', 'base_chip_value'],
            ascending=[False, False]
        ).groupby('value').head(n)

        totals = elegible.groupby('value').base_chip_value.sum()
        best_totals = totals.sort_values(ascending=False).drop_duplicates()

        return elegible[elegible.value.isin(best_totals[:1].index)]

    def draw_from_deck(self, deck, n=7):
        self.cards = pd.concat([self.cards, deck.cards[:n]])
        deck.cards = deck.cards[n:].copy()

    def find_best_high_card_hand(self):
        max_chip_value = self.cards.base_chip_value.max()
        return self.cards[self.cards.base_chip_value == max_chip_value]

    def find_best_pair_hand(self):
        return self._find_best_n_hand(2)

    def find_best_three_of_a_kind_hand(self):
        return self._find_best_n_hand(3)

    def find_best_four_of_a_kind_hand(self):
        return self._find_best_n_hand(4)

    def find_best_five_of_a_kind_hand(self):
        return self._find_best_n_hand(5)

    def find_best_two_pair_hand(self):
        value_count_list = self.cards.value.value_counts()

        if (value_count_list >= 2).any():
            pair_chips = []
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

    def find_best_full_house_hand(self):
        temp_hand = self.cards
    
        best_three = self.find_best_three_of_a_kind_hand()
        self.cards = self.cards.drop(best_three.index)
        best_pair = self.find_best_pair_hand()

        self.cards = temp_hand

        return pd.concat([best_pair, best_three])

    def find_best_flush_hand(self):
        pass

    def find_best_straight_hand(self):
        pass

    def find_best_straight_flush_hand(self):
        pass

    def find_best_flush_house_hand(self):
        pass

    def find_best_flush_five_hand(self):
        pass

    def find_best_poker_hand(self):
        pass
