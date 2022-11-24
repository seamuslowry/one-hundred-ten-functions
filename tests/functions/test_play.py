'''Playing a card unit tests'''
import json
from unittest import TestCase, mock

from models import RoundStatus
from play import main
from services import CardService
from tests.helpers import (USER_ONE, build_request, game, read_response_body,
                           return_input)


class TestPlay(TestCase):
    '''Card playing unit tests'''

    @mock.patch('services.GameService.save', side_effect=return_input)
    @mock.patch('services.GameService.get',
                return_value=game(RoundStatus.TRICKS))
    @mock.patch('services.UserService.from_request', mock.Mock(return_value=USER_ONE))
    @mock.patch('services.UserService.get', mock.Mock(return_value=USER_ONE))
    def test_bid(self, game_get, game_save):
        '''On hitting the plays endpoint, the logged in user plays the selected card'''
        original_hand = game_get.return_value.active_round.active_player.hand
        play_card = original_hand[0]

        req = build_request(
            route_params={'id': 'id'},
            body=json.dumps({'card': CardService.json(play_card)}).encode('utf-8'))

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        user_dict = next(
            (p for p in resp_dict['round']['players']
             if p['identifier'] == USER_ONE.identifier))
        new_hand = [CardService.from_client(c) for c in user_dict['hand']]

        game_save.assert_called_once()
        self.assertNotIn(play_card, new_hand)
        self.assertEqual(CardService.json(play_card), resp_dict['results'][0]['card'])
