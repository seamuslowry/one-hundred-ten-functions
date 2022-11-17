'''Person Service unit tests'''
from unittest import TestCase

from models import (Card, CardNumber, GameRole, Person, Player, RoundRole,
                    SelectableSuit)
from services import person


class TestPersonService(TestCase):
    '''Unit tests to ensure person translations work as expected'''

    def test_person_conversion(self):
        '''Person can be converted to and from a DB save'''
        initial_person = Person('', roles={GameRole.ORGANIZER})
        converted_person = person.person_from_db(person.to_db(initial_person))
        self.assertEqual(initial_person, converted_person)
        self.assertGreater(len(converted_person.roles), 0)

    def test_player_conversion(self):
        '''Player can be converted to and from a DB save'''
        initial_player = Player(
            '', roles={RoundRole.DEALER},
            hand=[Card(CardNumber.ACE, SelectableSuit.CLUBS)])
        converted_player = person.player_from_db(person.to_db(initial_player))
        self.assertEqual(initial_player, person.player_from_db(person.to_db(converted_player)))
        self.assertGreater(len(converted_player.roles), 0)
        self.assertGreater(len(converted_player.hand), 0)
