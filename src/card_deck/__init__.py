import enum


class Card:

    class Face(enum.Enum):
        pass

    class Suit(enum.Enum):
        pass

    @property
    def face(self):
        pass

    @property
    def suit(self):
        pass


class CardExtension(Card):

    class Face(enum.Enum):
        pass
        @property
        def order(self):
            if not hasattr(self, '_order_dict'):
                self._order_dict = {}
                for i, e in enumerate(type(self)):
                    self._order_dict[e] = i

            return self._order_dict[self]


    class Suit(enum.Enum):
        pass
        @property
        def order(self):
            if not hasattr(self, '_order_dict'):
                self._order_dict = {}
                for i, e in enumerate(type(self)):
                    self._order_dict[e] = i

            return self._order_dict[self]


    def __repr__(self):
        return '{}: {}, {}'.format(
            type(self), 
            self._face.value,
            self._suit.value
        )

    def __str__(self):
        return "{} of {}".format(
            self._face.value, 
            self._suit.value
        )


class GameDeck:

    @property
    def card_type(self):
        pass

    @property
    def deck(self):
        pass

    def shuffle(self):
        pass

    def deal(self) -> Card:
        pass
