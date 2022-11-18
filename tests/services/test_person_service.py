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

    def test_player_client_conversion_with_hand(self):
        '''Player will be sent to client with hand if matching the identifier'''
        initial_player = Player(
            '', roles={RoundRole.DEALER},
            hand=[Card(CardNumber.ACE, SelectableSuit.CLUBS)])
        client_player = person.json(initial_player, initial_player.identifier)
        self.assertIsNotNone(client_player)
        self.assertIn('hand', client_player)

    def test_player_client_conversion_with_mismatched_id(self):
        '''Player will be sent to client without their hand if not matching the identifier'''
        initial_player = Player(
            '', roles={RoundRole.DEALER},
            hand=[Card(CardNumber.ACE, SelectableSuit.CLUBS)])
        client_player = person.json(initial_player, initial_player.identifier + 'nomatch')
        self.assertIsNotNone(client_player)
        self.assertNotIn('hand', client_player)

    def test_player_client_conversion_with_no_id(self):
        '''Player will be sent to client without their hand if no identifier is passed'''
        initial_player = Player(
            '', roles={RoundRole.DEALER},
            hand=[Card(CardNumber.ACE, SelectableSuit.CLUBS)])
        client_player = person.json(initial_player)
        self.assertIsNotNone(client_player)
        self.assertNotIn('hand', client_player)

    def test_person_client_conversion(self):
        '''Person will be sent to client no hand always'''
        initial_person = Person(
            '', roles={GameRole.ORGANIZER})
        client_person = person.json(initial_person, initial_person.identifier)
        self.assertIsNotNone(client_person)
        self.assertNotIn('hand', client_person)
