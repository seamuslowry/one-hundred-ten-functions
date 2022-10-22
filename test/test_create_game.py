'''Create game unit tests'''
import json
import unittest

import azure.functions as func
from auth.user import User
from create_game import main


class TestCreateGame(unittest.TestCase):
    '''Create Game unit tests'''

    def test_run_without_auth(self):
        '''Test running the function without auth info'''
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/create_game'
        )

        resp = main(req)

        self.assertEqual(resp.get_body(),
                         User(None, None).to_json().encode('utf-8'))
