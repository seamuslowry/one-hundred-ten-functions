'''Create game unit tests'''
import json
from unittest import TestCase, mock

from app.models import Game
from create_game import main
from tests.helpers import (DEFAULT_USER, build_request, read_response_body,
                           return_input)


class TestCreateGame(TestCase):
    '''Create Game unit tests'''

    @mock.patch('app.services.GameService.save', side_effect=return_input)
    @mock.patch('create_game.parse_request',
                mock.Mock(return_value=(DEFAULT_USER, Game(), 0)))
    def test_creates_game(self, game_save):
        '''On hitting the create request a game is created and returned'''
        req = build_request(body=json.dumps({'name': 'test name'}).encode('utf-8'))

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertIsNotNone(resp_dict['id'])
