'''Request Parser unit tests'''
from unittest import TestCase, mock

from app.models import RoundStatus
from app.parsers import parse_request
from tests.helpers import DEFAULT_USER, build_request, game


class TestRequestParse(TestCase):
    '''Request parser unit tests'''

    def test_parses_without_game(self):
        '''Function returns without requesting a game'''
        (user, parsed_game) = parse_request(build_request())
        self.assertEqual(DEFAULT_USER, user)
        self.assertEqual('', parsed_game.name)

    # TODO fix
    # def test_parses_with_game(self):
    #     '''Function returns with a requested game'''
    #     (user, parsed_game) = parse_request(build_request(route_params={'game_id': 'id'}))
    #     self.assertEqual(DEFAULT_USER, user)
    #     self.assertEqual(get_game.return_value, parsed_game)
