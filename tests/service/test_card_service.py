'''Card Service unit tests'''
from unittest import TestCase

from hundredandten.constants import (CardNumber, SelectableSuit,
                                     UnselectableSuit)
from hundredandten.deck import Card

from service import card


class TestCardService(TestCase):
    '''Unit tests to ensure card translations work as expected'''

    def test_card_to_db(self):
        '''Card can be converted for DB save'''
        self.assertIsNotNone(card.to_db(
            Card(CardNumber.ACE, SelectableSuit.CLUBS)))

    def test_selectable_suit_card_from_db(self):
        '''Selectable suit card can be converted from DB save'''
        self.assertIsNotNone(card.from_db(
            card.to_db(Card(CardNumber.ACE, SelectableSuit.CLUBS))))

    def test_unselectable_suit_card_from_db(self):
        '''Unselectable suit card can be converted from DB save'''
        self.assertIsNotNone(card.from_db(
            card.to_db(Card(CardNumber.JOKER, UnselectableSuit.JOKER))))
