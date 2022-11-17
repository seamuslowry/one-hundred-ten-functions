'''User Service unit tests'''
import base64
import json
from unittest import TestCase

from models import GoogleUser, User
from services import UserService
from tests.helpers import build_request


class TestUserService(TestCase):
    '''Unit tests to ensure user operations work as expected'''

    def test_unknown_user(self):
        '''Init a user from an unknown source'''
        user = UserService.from_request(build_request())

        self.assertTrue(isinstance(user, User))
        self.assertFalse(isinstance(user, GoogleUser))

    def test_google_user(self):
        '''Init a user from Google'''
        user = UserService.from_request(
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

        self.assertRaises(ValueError, UserService.from_request, req)
