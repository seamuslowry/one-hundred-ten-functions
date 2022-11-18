'''Trick Service unit tests'''
from unittest import TestCase

from models import Card, CardNumber, Play, SelectableSuit, Trick
from services import trick


class TestTrickService(TestCase):
    '''Unit tests to ensure trick translations work as expected'''

    def test_trick_conversion(self):
        '''Trick can be converted to and from a DB save'''
        initial_trick = Trick(
            SelectableSuit.CLUBS,
            [Play('', Card(CardNumber.ACE, SelectableSuit.CLUBS))])

        self.assertEqual(initial_trick, trick.from_db(trick.to_db(initial_trick)))

    def test_trick_client_conversion(self):
        '''Trick can be converted to client value'''
        initial_trick = Trick(
            SelectableSuit.CLUBS,
            [Play('', Card(CardNumber.ACE, SelectableSuit.CLUBS))])

        self.assertIsNotNone(trick.json(initial_trick))
