'''Create game unit tests'''
from unittest import TestCase, mock

from auth.user import User
from create_game import main

from tests.helpers import build_request


class TestCreateGame(TestCase):
    '''Create Game unit tests'''

    @mock.patch('azure.functions.Out')
    def test_run(self, cosmos_mock):
        '''Test running the function without auth info'''
        req = build_request()

        resp = main(req, cosmos_mock)

        cosmos_mock.set.assert_called_once()
        self.assertEqual(resp.get_body(),
                         User(None, None).to_json().encode('utf-8'))
