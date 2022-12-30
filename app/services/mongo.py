'''A module to provide the mongo DB connection'''
import os

from pymongo import MongoClient
from pymongo.collection import Collection

connection_string = os.environ.get('MongoDb', '')
database_name = os.environ.get('DatabaseName', '')

mongo_client = MongoClient(connection_string)

# TODO create models that accurately map to the mongo objects and use here
m_game_client: Collection[dict] = mongo_client[database_name]['game']
m_user_client = mongo_client[database_name]['user']
