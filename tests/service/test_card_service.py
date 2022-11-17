'''Card Service unit tests'''
from unittest import TestCase

from models import Card, CardNumber, SelectableSuit, UnselectableSuit
from service import card


class TestCardService(TestCase):
    '''Unit tests to ensure card translations work as expected'''

    def test_selectable_suit_card_conversion(self):
        '''Selectable suit card can be converted to and from a DB save'''
        initial_card = Card(CardNumber.ACE, SelectableSuit.CLUBS)

        self.assertIsNotNone(initial_card, card.from_db(
            card.to_db(initial_card)))

    def test_unselectable_suit_card_from_db(self):
        '''Unselectable suit card can be converted from DB save'''
        initial_card = Card(CardNumber.JOKER, UnselectableSuit.JOKER)

        self.assertIsNotNone(initial_card, card.from_db(
            card.to_db(initial_card)))
