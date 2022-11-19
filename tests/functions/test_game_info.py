'''Get game unit tests'''
from unittest import TestCase, mock

from game_info import main
from models import Game, Group, Person
from tests.helpers import (DEFAULT_ID, DEFAULT_USER, build_request,
                           read_response_body, return_input)


class TestGameInfo(TestCase):
    '''Get Game unit tests'''

    @mock.patch('services.UserService.save', mock.Mock(side_effect=return_input))
    @mock.patch('services.GameService.get', mock.Mock(
        return_value=Game(people=Group([Person(DEFAULT_ID + 'no')]))))
    @mock.patch('services.UserService.get', mock.Mock(return_value=DEFAULT_USER))
    def test_get_game(self):
        '''On hitting the info endpoint the game is retrieved'''
        req = build_request(route_params={'id': 'id'})

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        self.assertIn('id', resp_dict)
