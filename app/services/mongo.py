'''A module to provide the mongo DB connection'''
import os

from pymongo import MongoClient
from pymongo.collection import Collection

from app.dtos import db

connection_string = os.environ.get('MongoDb', '')
database_name = os.environ.get('DatabaseName', '')

mongo_client = MongoClient(connection_string)

m_game_client: Collection[db.Game] = mongo_client[database_name]['game']
user_client: Collection[db.User] = mongo_client[database_name]['user']
