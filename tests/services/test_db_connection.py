'''Connecting to the DB unit tests'''
import importlib
import os
from unittest import TestCase, mock

import app.services.cosmos


class TestDbConnection(TestCase):
    '''Connect to DB unit tests'''

    @mock.patch('azure.cosmos.CosmosClient.from_connection_string')
    def test_doesnt_try_connect(self, try_connect):
        '''Won't try to connect if there's no connection string in the ENV'''
        importlib.reload(app.services.cosmos)

        try_connect.assert_not_called()

    @mock.patch.dict(os.environ, {"CosmosDb": "test"})
    @mock.patch('azure.cosmos.CosmosClient.from_connection_string')
    def test_does_try_connect(self, try_connect):
        '''Will try to connect if there's no connection string in the ENV'''
        importlib.reload(app.services.cosmos)

        try_connect.assert_called_once()
