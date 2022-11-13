'''Person Service unit tests'''
from unittest import TestCase

from hundredandten.group import Person, Player

from service import person


class TestPersonService(TestCase):
    '''Unit tests to ensure person translations work as expected'''

    def test_person_to_db(self):
        '''Person can be converted for DB save'''
        converted = person.to_db(Person(''))
        self.assertIsNotNone(converted)
        self.assertFalse('hand' in converted.keys())

    def test_player_to_db(self):
        '''Player can be converted for DB save'''
        converted = person.to_db(Player(''))
        self.assertIsNotNone(converted)
        self.assertTrue('hand' in converted.keys())
