'''Join game unit tests'''
from unittest import TestCase, mock

from app.models import Game, Group, Person
from join_game import main
from tests.helpers import (DEFAULT_ID, DEFAULT_USER, build_request,
                           read_response_body, return_input)


class TestJoinGame(TestCase):
    '''Join Game unit tests'''

    @mock.patch('app.services.GameService.save', side_effect=return_input)
    @mock.patch(
        'join_game.parse_request', mock.Mock(
            return_value=(DEFAULT_USER,
                          Game(people=Group([Person(DEFAULT_ID + 'no')])))))
    def test_joins_game(self, game_save):
        '''On hitting the join endpoint the logged in player joins the game'''
        req = build_request(route_params={'game_id': 'id'})

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertIn(DEFAULT_ID, map(lambda pd: pd['identifier'], resp_dict['players']))
