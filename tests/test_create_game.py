'''Create game unit tests'''
import unittest
import unittest.mock as mock

from auth.user import User
from create_game import main

from tests.helpers import build_request


class TestCreateGame(unittest.TestCase):
    '''Create Game unit tests'''

    URL = '/api/create_game'
    METHOD = 'GET'

    @mock.patch('azure.functions.Out')
    def test_run(self, cosmos_mock):
        '''Test running the function without auth info'''
        req = build_request()

        resp = main(req, cosmos_mock)

        cosmos_mock.set.assert_called_once()
        self.assertEqual(resp.get_body(),
                         User(None, None).to_json().encode('utf-8'))
