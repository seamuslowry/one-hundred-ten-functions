'''Trick Service unit tests'''
from unittest import TestCase

from hundredandten.actions import Play
from hundredandten.constants import CardNumber, SelectableSuit
from hundredandten.deck import Card
from hundredandten.trick import Trick

from service import trick


class TestTrickService(TestCase):
    '''Unit tests to ensure trick translations work as expected'''

    def test_trick_conversion(self):
        '''Trick can be converted to and from a DB save'''
        initial_trick = Trick(
            SelectableSuit.CLUBS,
            [Play('', Card(CardNumber.ACE, SelectableSuit.CLUBS))])

        self.assertEqual(initial_trick, trick.from_db(trick.to_db(initial_trick)))
