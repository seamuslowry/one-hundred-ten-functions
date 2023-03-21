'''Retrieve login unit tests'''
from time import time
from unittest import TestCase

from tests.helpers import put_user


class TestLogin(TestCase):
    '''Unit tests to create / update user as a client'''

    def test_create_user(self):
        '''Can create a new user'''
        identifier = f'{time()}'
        user = put_user(identifier)

        self.assertEqual(identifier, user['identifier'])

    def test_update_user(self):
        '''Can update an existing user'''
        identifier = f'{time()}'
        new_name = 'new_name'
        original_user = put_user(identifier, 'old_name')
        updated_user = put_user(identifier, new_name)

        self.assertEqual(original_user['identifier'], updated_user['identifier'])
        self.assertNotEqual(original_user['name'], updated_user['name'])
        self.assertEqual(new_name, updated_user['name'])
