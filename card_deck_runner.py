#!/usr/bin/env python3

import random

from french_card_deck import FrenchCardDeck

deck_of_cards = FrenchCardDeck()

##for card in deck_of_cards:
##    print(card)
##print()
##print()

##card = next(deck_of_cards)
##
##print(card.face)
##print(card.face.order)

deck_of_cards.shuffle()

for card in deck_of_cards:
    print(card)
print()
print()

deck_of_cards.sort()
deck_of_cards.reset_deck()

for card in deck_of_cards:
    print(card)
print()
print()
