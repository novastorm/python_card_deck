#!/usr/bin/env python3

import enum
import json
import random

from card_deck.french_card_deck import FrenchCardDeck, FrenchCard

Face = FrenchCard.Face
card_values = {
    Face.ace: 1,
    Face.two: 2,
    Face.three: 3,
    Face.four: 4,
    Face.five: 5,
    Face.six: 6,
    Face.seven: 7,
    Face.eight: 8,
    Face.nine: 9,
    Face.ten: 10,
    Face.jack: 10,
    Face.queen: 10,
    Face.king: 10
}

face_cards = set([
    Face.jack,
    Face.queen,
    Face.king
])

MAX_VALUE = 21
DEALER_MAX_HIT_VALUE = 17

class CardState(enum.Enum):
    down = 'down'
    up = 'up'

    def __str__(self):
        return self.value

    @property
    def serialize(self):
        return self.value


class BlackJackCard():

    @property
    def face(self):
        return self._card.face

    @property
    def suit(self):
        return self._card.suit

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_value):
        self._state = new_value

    @property
    def serialize(self):
        card = None
        if self.state == CardState.up:
            card = {
                'face': self.face.value,
                'suit': self.suit.value
            }
        return {
            'card': card,
            'state': self.state.serialize
        }

    def __init__(self, card, state=CardState.down):
        self._card = card
        self._state = state


class BlackJackHand():
    @property
    def card_list(self):
        return self._card_list

    @property
    def value(self):
        return self._value

    @property
    def is_soft(self):
        return self._is_soft

    @property
    def serialize(self):
        return [card.serialize for card in self.card_list]

    def __init__(self):
        self._card_list = []
        self.clear_card_list()

    def add_card(self, card):
        self._card_list.append(BlackJackCard(card))
        self._calculate_value()

    def clear_card_list(self):
        self._card_list.clear()
        self._value = None
        self._is_soft = None

    def _calculate_value(self):
        value = 0
        number_of_aces = 0
        is_soft = False
        for card in self.card_list:
            if card.face == Face.ace:
                number_of_aces += 1
            value += card_values[card.face]

        for i in range(number_of_aces):
            if value + 10 <= MAX_VALUE:
                value += 10
                is_soft = True

        self._value = value
        self._is_soft = is_soft

    def __getitem__(self, key):
        return self.card_list[key]


class BlackJackPlayer():
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_value):
        self._name = new_value

    @property
    def hand(self):
        return self._hand

    @property
    def serialize(self):
        return {
            'name': self.name,
            'hand': self.hand.serialize
        }

    def add_card(self, card):
        self._hand.add_card(card)

    def clear_hand(self):
        self._hand.clear_card_list()

    def __init__(self, name=None):
        self._hand = BlackJackHand()
        self._name = name


class BlackJackGame():

    @property
    def shuffle_card_percentage(self):
        return self._shuffle_card_percentage

    @shuffle_card_percentage.setter
    def shuffle_card_percentage(self, new_value):
        self._shuffle_card_percentage = new_value

    @property
    def serialize(self):
        return {
            'dealer': self._dealer.serialize,
            'players': [player.serialize if player else player for player in self._players]
        }   

    def __init__(self):
        self._deck = FrenchCardDeck()
        self._shuffle_card_percentage = 0.5
        self._shuffle_card_index = None
        self._is_last_hand = False
        self._dealer = BlackJackPlayer('Dealer')
        self._players = [None] * 7
    
        self._shuffle()

    def add_player(self, player, position):
        if self._players[position] is not None:
            return False
    
        self._players[position] = player
        return True

    def remove_player_at_position(position):
        self._players[position] = None

    def _shuffle(self):
        print('shuffle')
        self._deck.shuffle()
        self._shuffle_card_index = int(self._deck.total_number_of_cards * self._shuffle_card_percentage) + random.randint(-5, 5)
        self._is_last_hand = False

    def _deal(self, player):
        card = self._deck.deal()
        player.add_card(card)

    def deal_starting_hands(self):
        self._deal(self._dealer)
        self._dealer.hand.card_list[0].state = CardState.up
        for player in self._players:
            if player is None:
                continue
            self._deal(player)
        self._deal(self._dealer)
        for player in self._players:
            if player is None:
                continue
            self._deal(player)
   
    def __str__(self):
        return str(self.serialize)


def start_game():
    deck = FrenchCardDeck()
    while True:
        play_game(deck)
        response = input("Leave table?? (y/N): ")
        if response.lower() == 'y':
            break
    print("Come again sooni!")

def play_game(deck):
    cut_card_index = None

    while True:
        print('cci:', cut_card_index, 'ci:', deck.card_index)
        if cut_card_index is None or deck.card_index > cut_card_index:
            print("Shuffle")
            deck.shuffle()
            cut_card_index = int(deck.total_number_of_cards * 4 / 5) + random.randint(-7, 2)
            print('cci:', cut_card_index, 'ci:', deck.card_index)
        dealer_hand = [deck.deal()]
        player_hand = [deck.deal()]

        dealer_hand.append(deck.deal())
        player_hand.append(deck.deal())

        dealer_hand_value, dealer_hand_is_soft = calculate_value_of_hand(dealer_hand)
        if dealer_hand[0].face == Face.ace:
            pass
        if dealer_hand_value == MAX_VALUE and player_hand_value != MAX_VALUE:
            print("Player:", [str(card) for card in player_hand], player_hand_value)
            print("Dealer:", [str(card) for card in dealer_hand], dealer_hand_value)
            print("Better luck next time")
            break
            
        while True:
            player_hand_value, player_hand_is_soft = calculate_value_of_hand(player_hand)
            print('Dealer:', [str(dealer_hand[0]), '*'])
            print('Player:', [str(card) for card in player_hand], player_hand_value)
            if player_hand_value >= MAX_VALUE:
                if player_hand_value > MAX_VALUE:
                    print("Player Bust")
                break
            response = None
            while True:
                response = input('(H)it or (S)tand: ')
                if response.lower() in ('h', 's'):
                    break
            if response.lower() == 's':
                break
            player_hand.append(deck.deal())

        print("Dealer:", [str(card) for card in dealer_hand], dealer_hand_value)
        if not (player_hand_value > MAX_VALUE or len(player_hand) == 2 and player_hand_value == MAX_VALUE and dealer_hand != MAX_VALUE):
            while (dealer_hand_value < DEALER_MAX_HIT_VALUE or 
                    dealer_hand_value == DEALER_MAX_HIT_VALUE and dealer_hand_is_soft):
                dealer_hand.append(deck.deal())
                dealer_hand_value, dealer_hand_is_soft = calculate_value_of_hand(dealer_hand)
                print("Dealer:", [str(card) for card in dealer_hand], dealer_hand_value)
            if dealer_hand_value > MAX_VALUE:
                print("Dealer Bust")

        if player_hand_value == dealer_hand_value:
            print("Push")
        elif player_hand_value <= MAX_VALUE and (dealer_hand_value > MAX_VALUE or player_hand_value > dealer_hand_value):
            print("Winner")
        else: # player_hand_value < dealer_hand_value:
            print("Better luck next time")

        response = input("Play again? (Y/n): ")
        if response.lower() == 'n':
            break

def calculate_value_of_hand(hand):
    value = 0
    number_of_aces = 0
    is_soft = False
    for card in hand:
        if card.face == Face.ace:
            number_of_aces += 1
        value += card_values[card.face]

    for i in range(number_of_aces):
        if value + 10 <= MAX_VALUE:
            value += 10
            is_soft = True

    return (value, is_soft)
        


#start_game()
game = BlackJackGame()
print(game)

player1 = BlackJackPlayer('Player 1')
game.add_player(player1, 1)
print(game)

game.deal_starting_hands()
print()
print(game)

print()
print(json.dumps(game.serialize, sort_keys=True, indent=2))

