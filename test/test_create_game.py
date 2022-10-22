'''Create game unit tests'''
import unittest
from test.helpers import build_request

from auth.user import User
from create_game import main


class TestCreateGame(unittest.TestCase):
    '''Create Game unit tests'''

    URL = '/api/create_game'
    METHOD = 'GET'

    def test_run(self):
        '''Test running the function without auth info'''
        req = build_request()

        resp = main(req)

        self.assertEqual(resp.get_body(),
                         User(None, None).to_json().encode('utf-8'))
