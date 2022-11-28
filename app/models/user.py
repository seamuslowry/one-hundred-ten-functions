'''Model user-related information.'''


from dataclasses import dataclass, field


@dataclass
class User:
    '''A class to interact with generic users'''
    identifier: str
    name: str = field(compare=False)

    def __init__(self, identifier: str, name: str):
        self.identifier = identifier
        self.name = name


@dataclass
class GoogleUser(User):
    '''A class to interact with Google authenticated users'''
    picture_url: str = field(compare=False)
