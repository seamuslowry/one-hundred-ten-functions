'''Request Parser unit tests'''
from unittest import TestCase, mock

from app.models import RoundStatus
from app.parsers import parse_request
from tests.helpers import DEFAULT_USER, build_request, game


class TestRequestParse(TestCase):
    '''Request parser unit tests'''

    @mock.patch('app.services.UserService.from_request', mock.Mock(return_value=DEFAULT_USER))
    def test_parses_without_game(self):
        '''Function returns without requesting a game'''
        (user, parsed_game, count) = parse_request(build_request())
        self.assertEqual(DEFAULT_USER, user)
        self.assertEqual('', parsed_game.name)
        self.assertEqual(0, count)

    @mock.patch('app.services.GameService.get', return_value=game(RoundStatus.BIDDING))
    @mock.patch('app.services.UserService.from_request', mock.Mock(return_value=DEFAULT_USER))
    def test_parses_with_game(self, get_game):
        '''Function returns with a requested game'''
        (user, parsed_game, count) = parse_request(build_request(route_params={'id': 'id'}))
        self.assertEqual(DEFAULT_USER, user)
        self.assertEqual(get_game.return_value, parsed_game)
        self.assertEqual(len(get_game.return_value.events), count)
