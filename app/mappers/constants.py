'''Constants to support DB mapping'''
from enum import Enum


class UserType(str, Enum):
    '''Enum value for user type'''
    GOOGLE = "google"
    UNKNOWN = "unknown"
