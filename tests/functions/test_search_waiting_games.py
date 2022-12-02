'''Games in lobby unit tests'''
import json
from unittest import TestCase, mock

from app.models import Game
from app.services import GameService
from search_waiting_games import main
from tests.helpers import DEFAULT_USER, build_request, read_response_body


class TestSearchWaitingGames(TestCase):
    '''Search Lobby Game unit tests'''

    @mock.patch('search_waiting_games.parse_request',
                mock.Mock(return_value=(DEFAULT_USER, Game())))
    @mock.patch('app.services.GameService.search_waiting', return_value=[Game()])
    def test_get_game(self, search_games):
        '''On hitting the lobby games endpoint games are retrieved'''
        req = build_request(body=json.dumps({'gameRole': 'ORGANIZER'}).encode('utf-8'))

        resp = main(req)
        resp_list = read_response_body(resp.get_body())

        self.assertEqual(list(map(lambda g: GameService.json(
            g, ''), search_games.return_value)), resp_list)
