'''User Service unit tests'''
import base64
import json
from unittest import TestCase

from models import GoogleUser, User
from services import UserService
from services.cosmos import user_client
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
        user_client.upsert_item.return_value = {
            'type': 'google', 'id': '', 'name': '', 'picture_url': ''}

        user = UserService.from_request(
            build_request(
                headers={'x-ms-client-principal-idp': 'google',
                         'x-ms-client-principal': base64.b64encode(json.dumps({'claims': []})
                                                                   .encode()).decode()}))
        self.assertTrue(isinstance(user, User))
        self.assertTrue(isinstance(user, GoogleUser))

        user_client.upsert_item.reset_mock(return_value=True)

    def test_invalid_user(self):
        '''Do not allow initializing an invalid user'''
        req = build_request(
            headers={'x-ms-client-principal-idp': ''})

        self.assertRaises(ValueError, UserService.from_request, req)

    def test_search_user(self):
        '''Searches for users'''
        users = UserService.search('text')

        self.assertIsNotNone(users)
        user_client.query_items.assert_called_once()

    def test_serializes_user(self):
        '''Serializes a user'''
        self.assertIsNotNone(UserService.json(User('', '')))
