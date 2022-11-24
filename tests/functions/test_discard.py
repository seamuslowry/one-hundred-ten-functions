'''Discarding unit tests'''
import json
from unittest import TestCase, mock

from discard import main
from models import RoundStatus
from services import CardService
from tests.helpers import (DEFAULT_USER, build_request, game,
                           read_response_body, return_input)


class TestDiscard(TestCase):
    '''Discarding unit tests'''

    @mock.patch('services.GameService.save', side_effect=return_input)
    @mock.patch('services.GameService.get',
                return_value=game(RoundStatus.DISCARD))
    @mock.patch('services.UserService.from_request', mock.Mock(return_value=DEFAULT_USER))
    @mock.patch('services.UserService.get', mock.Mock(return_value=DEFAULT_USER))
    def test_distard(self, game_get, game_save):
        '''On hitting the discard endpoint, the logged in user discards the provided cards'''
        original_hand = game_get.return_value.active_round.active_player.hand

        req = build_request(route_params={'id': 'id'}, body=json.dumps({'cards': [CardService.json(
            c) for c in original_hand]}).encode('utf-8'))

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        user_dict = next(
            (p for p in resp_dict['round']['players']
             if p['identifier'] == DEFAULT_USER.identifier))
        new_hand = [CardService.from_client(c) for c in user_dict['hand']]

        game_save.assert_called_once()
        self.assertNotEqual(original_hand, new_hand)
        self.assertEqual(DEFAULT_USER.identifier, resp_dict['events'][0]['identifier'])
