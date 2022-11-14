'''Person Service unit tests'''
from unittest import TestCase

from hundredandten.constants import (CardNumber, GameRole, RoundRole,
                                     SelectableSuit)
from hundredandten.deck import Card
from hundredandten.group import Person, Player

from service import person


class TestPersonService(TestCase):
    '''Unit tests to ensure person translations work as expected'''

    def test_person_conversion(self):
        '''Person can be converted to and from a DB save'''
        initial_person = Person('', roles={GameRole.ORGANIZER})
        self.assertEqual(initial_person, person.person_from_db(person.to_db(initial_person)))

    def test_player_conversion(self):
        '''Player can be converted to and from a DB save'''
        initial_player = Player(
            '', roles={RoundRole.DEALER},
            hand=[Card(CardNumber.ACE, SelectableSuit.CLUBS)])
        self.assertEqual(initial_player, person.player_from_db(person.to_db(initial_player)))
