'''Trick Service unit tests'''
from unittest import TestCase

from hundredandten.actions import Play
from hundredandten.constants import CardNumber, SelectableSuit
from hundredandten.deck import Card
from hundredandten.trick import Trick

from service import trick


class TestTrickService(TestCase):
    '''Unit tests to ensure trick translations work as expected'''

    def test_trick_to_db(self):
        '''Trick can be converted for DB save'''
        self.assertIsNotNone(trick.to_db_dict(
            Trick(
                SelectableSuit.CLUBS,
                [Play('', Card(CardNumber.ACE, SelectableSuit.CLUBS))])))
