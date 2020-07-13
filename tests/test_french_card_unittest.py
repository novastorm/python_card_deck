import unittest
from card_deck.french_card_deck import FrenchCard, FrenchCardDeck

class FrenchCard_TestCase(unittest.TestCase):

    def test_faces(self):
        expected = [
            'ace',
            'two',
            'three',
            'four',
            'five',
            'six',
            'seven',
            'eight',
            'nine',
            'ten',
            'jack',
            'queen',
            'king'
        ]

        result = [
            e.value for e in FrenchCard.Face
        ]

        self.assertEqual(result, expected)

    def test_suits(self):
        expected = [
            'spades',
            'hearts',
            'clubs',
            'diamonds'
        ]

        result = [
            e.value for e in FrenchCard.Suit
        ]

        self.assertEqual(result, expected)

    def test_order(self):
        deck = FrenchCardDeck()

        for suit in FrenchCard.Suit:
            for face in FrenchCard.Face:
                card = deck.deal()
                self.assertEqual(card.suit, suit)
                self.assertEqual(card.face, face) 

    @unittest.expectedFailure
    def test_random(self):
        deck = FrenchCardDeck()

        deck.shuffle()

        for suit in FrenchCard.Suit:
            for face in FrenchCard.Face:
                card = deck.deal()
                self.assertEqual(card.suit, suit)
                self.assertEqual(card.face, face) 
        

if __name__ == '__main__':
    unittest.main()

