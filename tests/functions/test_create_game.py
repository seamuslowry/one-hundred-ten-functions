'''Create game unit tests'''
from unittest import TestCase, mock

from create_game import main
from tests.helpers import build_request, read_response_body


class TestCreateGame(TestCase):
    '''Create Game unit tests'''

    @mock.patch('azure.functions.Out')
    def test_creates_game(self, cosmos_mock):
        '''On hitting the create request a game is created and returned'''
        req = build_request()

        resp = main(req, cosmos_mock)

        cosmos_mock.set.assert_called_once()
        self.assertIsNotNone(read_response_body(resp.get_body())['id'])
