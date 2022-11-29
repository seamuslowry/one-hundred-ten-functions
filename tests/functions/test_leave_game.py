'''Leave game unit tests'''
from unittest import TestCase, mock

from app.models import Game, Group, Person, Player, Round, RoundRole
from leave_game import main
from tests.helpers import (DEFAULT_ID, build_request, read_response_body,
                           return_input)


class TestLeaveGame(TestCase):
    '''Leave Game unit tests'''

    @mock.patch('app.services.GameService.save', side_effect=return_input)
    @mock.patch('app.services.UserService.save', mock.Mock(side_effect=return_input))
    @mock.patch('app.services.GameService.get', mock.Mock(
        return_value=Game(
            people=Group([Person(DEFAULT_ID),
                          Person(DEFAULT_ID + '2')]))))
    def test_leaves_game(self, game_save):
        '''On hitting the leave endpoint in an unstarted game, the player leaves the game'''
        req = build_request(route_params={'id': 'id'})

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertNotIn(DEFAULT_ID, map(lambda pd: pd['identifier'], resp_dict['players']))

    @mock.patch('app.services.GameService.save', side_effect=return_input)
    @mock.patch('app.services.UserService.save', mock.Mock(side_effect=return_input))
    @mock.patch(
        'app.services.GameService.get', mock.Mock(
            return_value=Game(
                people=Group([]),
                rounds=[
                    Round(
                        players=Group(
                            [Player(identifier=DEFAULT_ID, roles={RoundRole.DEALER}),
                             Player(identifier=DEFAULT_ID + '2')]))])))
    def test_automates_player(self, game_save):
        '''On hitting the leave endpoint in an started game, the player is automated'''
        req = build_request(route_params={'id': 'id'})

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        player_dict = resp_dict['round']['dealer']

        self.assertTrue(player_dict['automate'])
