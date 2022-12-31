'''Facilitate interaction with the user DB'''

from enum import Enum

import azure.functions as func

from app.mappers import client, db
from app.models import User
from app.services.mongo import m_user_client


class UserType(str, Enum):
    '''Enum value for partition keys'''
    GOOGLE = "google"
    UNKNOWN = "unknown"


MAX = 20


def from_request(req: func.HttpRequest) -> User:
    '''Create a user object from a passed request'''
    return save(client.deserialize.user(req))


def save(user: User) -> User:
    '''Save the provided user to the DB'''
    m_user_client.update_one(
        {'identifier': user.identifier},
        {'$set': db.serialize.user(user)},
        upsert=True)
    return user


def search(search_text: str) -> list[User]:
    '''Retrieve the users with names like the provided'''
    return list(
        map(db.deserialize.user, m_user_client.find(
            {'name': {'$regex': search_text, '$options': 'i'}}).limit(MAX)))


def by_identifiers(identifiers: list[str]) -> list[User]:
    '''Retrieve the users with identifiers in the list provided'''
    return list(
        map(db.deserialize.user, m_user_client.find(
            {'identifier': {'$in': identifiers}}).limit(MAX)))
