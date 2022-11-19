'''Join game unit tests'''
from unittest import TestCase, mock

from join_game import main
from models import Game
from tests.helpers import (DEFAULT_ID, build_request, read_response_body,
                           return_input)


class TestJoinGame(TestCase):
    '''Join Game unit tests'''

    @mock.patch('services.GameService.save', side_effect=return_input)
    @mock.patch('services.UserService.save', mock.Mock(side_effect=return_input))
    @mock.patch('services.GameService.get', mock.Mock(return_value=Game()))
    def test_joins_game(self, game_save):
        '''On hitting the join endpoint the logged in player joins the game'''
        req = build_request(route_params={'id': 'id'})

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertIn(DEFAULT_ID, map(lambda pd: pd['identifier'], resp_dict['players']))
