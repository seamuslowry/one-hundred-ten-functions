'''Superclass to mark sub-class as serializable'''
import json


class Serializable():
    '''Add a to_json method to subclasses'''

    def to_json(self):
        '''Return a JSON representation of the object'''
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
