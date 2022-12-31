'''Format of a game of Hundred and Ten on the client'''

from typing import Optional, TypedDict


class User(TypedDict):
    '''A class to model the client format of a Hundred and Ten user'''
    identifier: str
    name: str
    picture_url: Optional[str]
