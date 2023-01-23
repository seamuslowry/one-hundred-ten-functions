'''Ensure edge cases of mapping are unit tested'''
import base64
import json
from unittest import TestCase

import azure.functions as func

from app.mappers.client import deserialize, serialize
from app.mappers.constants import UserType
from app.models import Action
from app.models.user import GoogleUser


class TestMapperEdgeCases(TestCase):
    '''Unit tests to ensure mapper edge cases behave as expected'''

    def test_bad_suggestion_error(self):
        '''Attempting to serialize an invalid suggestion results in an error'''
        identifier = 'identifier'
        self.assertRaises(ValueError, serialize.suggestion, Action(identifier), identifier)

    def test_incomplete_user_info(self):
        '''Attempting to serialize a user with incomplete header info results in an error'''
        self.assertRaises(ValueError, deserialize.user, func.HttpRequest(
            method='GET',
            body=b'',
            url='',
            headers={
                'x-ms-client-principal-idp': UserType.GOOGLE
            }
        ))

    def test_default_user_info(self):
        '''Attempting to serialize a user with incomplete user info defaults to empty string'''
        user = deserialize.user(func.HttpRequest(
            method='GET',
            body=b'',
            url='',
            headers={'x-ms-client-principal-idp': UserType.GOOGLE,
                     'x-ms-client-principal-id': 'name',
                     'x-ms-client-principal-name': 'name',
                     'x-ms-client-principal': base64.b64encode(
                         json.dumps(
                             {
                                 'claims': []
                             }).encode('utf-8')).decode('utf-8')}
        ))

        assert isinstance(user, GoogleUser)
        self.assertEqual('', user.name)
        self.assertEqual('', user.picture_url)
