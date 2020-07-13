import random

import card_deck

from card_deck import GameDeck

class Card(card_deck.CardExtension, card_deck.Card):
    pass

class FrenchCard(Card):
    class Face(Card.Face):
        ace = 'ace'
        two = 'two'
        three = 'three'
        four = 'four'
        five = 'five'
        six = 'six'
        seven = 'seven'
        eight = 'eight'
        nine = 'nine'
        ten = 'ten'
        jack = 'jack'
        queen = 'queen'
        king = 'king'


    class Suit(Card.Suit):
        spades = 'spades'
        hearts = 'hearts'
        clubs = 'clubs'
        diamonds = 'diamonds'

    @property
    def face(self) -> Card.Face:
        return self._face

    @property
    def suit(self) -> Card.Suit:
        return self._suit

    def __init__(self, face: Card.Face, suit: Card.Suit):
        self._face = face
        self._suit = suit


class FrenchCardDeck(GameDeck):

    _card_type = FrenchCard

    @property
    def card_type(self):
        return self._card_type

    @property
    def deck(self):
        return self._deck

    @property
    def number_of_decks(self):
        return self._number_of_decks

    @property
    def total_number_of_cards(self):
        if not hasattr(self, '_total_number_of_cards'):
            number_of_suits = len(self._card_type.Suit)
            number_of_faces = len(self._card_type.Face)
            self._total_number_of_cards = (
                len(self._card_type.Suit) *
                len(self._card_type.Face) *
                self._number_of_decks
            )
        return self._total_number_of_cards

    @property
    def card_index(self):
        return self._card_index

    @classmethod
    def generate_card_deck(cls, number_of_decks=1):
        a_deck = cls()
        a_deck.generate_cards
        
    def __init__(self, number_of_decks=1):
        self._number_of_decks = number_of_decks

        self._generate_main_deck()
        self.generate_cards()
        self._card_index = 0

    def _generate_main_deck(self):
        main_deck = []

        card_suit_list = list(self._card_type.Suit)
        card_face_list = list(self._card_type.Face)

        for suit in card_suit_list:
            for face in card_face_list:
                main_deck.append(
                    FrenchCard(face, suit)
                )
        self._main_deck = tuple(main_deck)

    def generate_cards(self):
        a_deck = []
        for i in range(self._number_of_decks):
            a_deck.extend(self._main_deck)
        self._deck = a_deck

    def shuffle(self):
        self._card_index = 0
        random.shuffle(self._deck)

    def deal(self):
        return next(self)

    def reset_deck(self):
        self._card_index = 0

    def sort(self):
        def key(r):
            return (r.suit.order, r.face.order)
        self._deck.sort(key=key)
            
    def __iter__(self):
        return self

    def __next__(self):
        card_index = self._card_index
        self._card_index += 1
        if card_index >= self.total_number_of_cards:
            raise StopIteration
        return self.deck[card_index]
    
