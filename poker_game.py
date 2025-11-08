# poker game
from enum import Enum
import random


class Suit(Enum):
    SPADE, HEART, CLUB, DIAMOND = range(4)


class Card:
    def __init__(self, suit: Suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.suit}{self.rank}"

    def __lt__(self, other):
        if self.rank == other.rank:
            return self.suit.value < other.suit.value
        else:
            return self.rank < other.rank


class Deck:
    def built(self):
        return [Card(suit, rank) for suit in Suit for rank in range(1, 14)]

    def __init__(self):
        self.cards = self.built()
        random.shuffle(self.cards)

    def deal_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None


class Player:
    def __init__(
        self,
        name,
    ):
        self.name = name
        self.hand = []

    def add_card(self, card):
        if card:
            self.hand.append(card)


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = [Player(1), Player(2), Player(3)]
