'''Card Service unit tests'''
from unittest import TestCase

from models import Card, CardNumber, SelectableSuit, UnselectableSuit
from services import card


class TestCardService(TestCase):
    '''Unit tests to ensure card translations work as expected'''

    def test_selectable_suit_card_conversion(self):
        '''Selectable suit card can be converted to and from a DB save'''
        initial_card = Card(CardNumber.ACE, SelectableSuit.CLUBS)

        self.assertEqual(initial_card, card.from_db(
            card.to_db(initial_card)))

    def test_unselectable_suit_card_conversion(self):
        '''Unselectable suit card can be converted from DB save'''
        initial_card = Card(CardNumber.JOKER, UnselectableSuit.JOKER)

        self.assertEqual(initial_card, card.from_db(
            card.to_db(initial_card)))

    def test_card_client_conversion(self):
        '''Card can be converted to client value'''
        initial_card = Card(CardNumber.JOKER, UnselectableSuit.JOKER)

        self.assertIsNotNone(card.json(initial_card))
