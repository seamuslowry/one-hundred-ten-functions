'''Lobby Game unit tests'''
from unittest import TestCase

import create_game
from app.dtos.client import WaitingGame
from tests.helpers import build_request, read_response_body


class TestLobbyGame(TestCase):
    '''Unit tests to ensure games that are waiting for players work as expected'''

    def test_create_game(self):
        '''New game can be created'''
        organizer = 'organizer'
        resp = create_game.main(
            build_request(
                headers={'x-ms-client-principal-id': organizer},
                body={'name': 'test name'}))
        game: WaitingGame = read_response_body(resp.get_body())

        self.assertEqual(organizer, game['organizer']['identifier'])
