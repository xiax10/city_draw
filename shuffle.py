'''Poker cards shuffle'''

import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

def Pokerstack():
    cards = [Card('1', 'spades'), Card('1', 'clubs'), Card('2', 'spades'), Card('3', 'spades')]
    return cards

cards = Pokerstack()
random.shuffle(cards)

for item in cards:
    print(item.rank + ' of ' + item.suit)