'''Person Service unit tests'''
from unittest import TestCase

from hundredandten.constants import GameRole, RoundRole
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

    def test_person_from_db(self):
        '''Person can be converted from DB save'''
        from_db = person.person_from_db(person.to_db(Person('', roles={GameRole.ORGANIZER})))
        self.assertIsNotNone(from_db)
        self.assertIsInstance(from_db, Person)

    def test_player_from_db(self):
        '''Player can be converted from DB save'''
        from_db = person.player_from_db(person.to_db(Player('', roles={RoundRole.DEALER})))
        self.assertIsNotNone(from_db)
        self.assertIsInstance(from_db, Player)
