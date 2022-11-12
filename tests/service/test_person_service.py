'''Game Service unit tests'''
from unittest import TestCase

from hundredandten.group import Person

from service import person


class TestPersonService(TestCase):
    '''Unit tests to ensure person translations work as expected'''

    def test_game_to_db(self):
        '''HundredAndTen can be converted for DB save'''
        self.assertIsNotNone(person.to_db_dict(Person('')))
