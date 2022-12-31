'''A module to convert models to client objects'''

from app import models
from app.dtos import client


def user(m_user: models.User) -> client.User:
    '''Return users as they can be provided to the client'''
    return client.User(
        identifier=m_user.identifier,
        name=m_user.name,
        picture_url=m_user.picture_url if isinstance(m_user, models.GoogleUser) else None
    )
