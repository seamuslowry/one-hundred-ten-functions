'''Get game players unit tests'''
from unittest import TestCase, mock

from app.models import Game, Group, Person
from app.services import UserService
from players import main
from tests.helpers import (DEFAULT_ID, DEFAULT_USER, USER_ONE, build_request,
                           read_response_body)


class TestGameInfo(TestCase):
    '''Get players unit tests'''

    @mock.patch('players.parse_request',
                mock.Mock(return_value=(DEFAULT_USER,
                                        Game(people=Group([Person(DEFAULT_ID + 'no')])))))
    @mock.patch('app.services.UserService.by_identifiers',
                return_value=[DEFAULT_USER, USER_ONE])
    def test_get_players(self, get_users):
        '''On hitting the players endpoint the players are retrieved'''
        req = build_request(route_params={'game_id': 'id'})

        resp = main(req)
        resp_list = read_response_body(resp.get_body())

        # TODO fix
        # self.assertEqual(list(map(UserService.json, get_users.return_value)), resp_list)
