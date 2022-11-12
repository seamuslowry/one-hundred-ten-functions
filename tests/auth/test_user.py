'''User unit tests'''
import base64
import json
import unittest

from auth.user import GoogleUser, User
from tests.helpers import build_request


class TestUser(unittest.TestCase):
    '''User unit tests'''

    def test_unknown_user(self):
        '''Init a user from an unknown source'''
        user = User.from_request(build_request())

        self.assertTrue(isinstance(user, User))
        self.assertFalse(isinstance(user, GoogleUser))

    def test_google_user(self):
        '''Init a user from Google'''
        user = User.from_request(
            build_request(
                headers={'x-ms-client-principal-idp': 'google',
                         'x-ms-client-principal': base64.b64encode(json.dumps({'claims': []})
                                                                   .encode()).decode()}))

        self.assertTrue(isinstance(user, User))
        self.assertTrue(isinstance(user, GoogleUser))

    def test_invalid_user(self):
        '''Do not allow initializing an invalid user'''
        req = build_request(
            headers={'x-ms-client-principal-idp': ''})

        self.assertRaises(ValueError, User.from_request, req)
