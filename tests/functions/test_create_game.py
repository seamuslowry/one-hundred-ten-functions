'''Create game unit tests'''
import json
from unittest import TestCase, mock

from create_game import main
from tests.helpers import build_request, read_response_body, return_input


class TestCreateGame(TestCase):
    '''Create Game unit tests'''

    @mock.patch('services.GameService.save', side_effect=return_input)
    @mock.patch('services.UserService.save', side_effect=return_input)
    def test_creates_game(self, game_save, user_save):
        '''On hitting the create request a game is created and returned'''
        req = build_request(body=json.dumps({'name': 'test name'}).encode('utf-8'))

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        user_save.assert_called_once()
        self.assertIsNotNone(resp_dict['id'])
