'''A module to provide the cosmos DB connection'''
import os
from unittest.mock import MagicMock

from azure.cosmos import ContainerProxy, CosmosClient

connection_string = os.environ.get('CosmosDb', '')
database_name = os.environ.get('DatabaseName', '')

if connection_string:
    cosmos_client = CosmosClient.from_connection_string(connection_string)
    game_client: ContainerProxy = cosmos_client.get_database_client(
        database_name).get_container_client('game')
    user_client: ContainerProxy = cosmos_client.get_database_client(
        database_name).get_container_client('user')
else:
    game_client = MagicMock(ContainerProxy)
    user_client = MagicMock(ContainerProxy)
