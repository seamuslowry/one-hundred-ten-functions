'''Get game unit tests'''
from unittest import TestCase, mock

from app.models import Game, Group, Person
from game_info import main
from tests.helpers import (DEFAULT_ID, DEFAULT_USER, build_request,
                           read_response_body)


class TestGameInfo(TestCase):
    '''Get Game unit tests'''

    @mock.patch('game_info.parse_request',
                mock.Mock(return_value=(DEFAULT_USER,
                                        Game(people=Group([Person(DEFAULT_ID + 'no')])))))
    def test_get_game(self):
        '''On hitting the info endpoint the game is retrieved'''
        req = build_request(route_params={'id': 'id'})

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        self.assertIn('id', resp_dict)
        self.assertNotIn('results', resp_dict)
