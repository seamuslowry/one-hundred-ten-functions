'''Playing Game unit tests'''
from unittest import TestCase

import bid
import create_game
import discard
import play
import rescind_prepass
import select_trump
import start_game
import suggestion
from app.dtos.client import PlaySuggestion, StartedGame, WaitingGame
from app.models import BidAmount, RoundStatus, SelectableSuit
from tests.helpers import build_request, read_response_body


class TestPlayingGame(TestCase):
    '''Unit tests to ensure games that are in progress behave as expected'''

    def get_initial_game(self) -> StartedGame:
        '''Get a started game waiting for the first move'''
        resp = create_game.main(
            build_request(
                body={'name': 'play round test'}))
        created_game: WaitingGame = read_response_body(resp.get_body())
        resp = start_game.main(
            build_request(
                route_params={'game_id': created_game['id']},
                headers={'x-ms-client-principal-id': created_game['organizer']['identifier']}))
        return read_response_body(resp.get_body())

    def test_perform_round_actions(self):
        '''A round of the game can be played'''
        created_game: StartedGame = self.get_initial_game()
        self.assertEqual(RoundStatus.BIDDING.name, created_game['status'])

        # bid
        resp = bid.main(
            build_request(
                route_params={'game_id': created_game['id']},
                body={
                    'amount': BidAmount.SHOOT_THE_MOON
                })
        )
        game: StartedGame = read_response_body(resp.get_body())

        self.assertEqual(RoundStatus.TRUMP_SELECTION.name, game['status'])

        # select trump
        resp = select_trump.main(
            build_request(
                route_params={'game_id': created_game['id']},
                body={
                    'suit': SelectableSuit.CLUBS.name
                })
        )
        game: StartedGame = read_response_body(resp.get_body())

        self.assertEqual(RoundStatus.DISCARD.name, game['status'])

        # discard
        resp = discard.main(
            build_request(
                route_params={'game_id': created_game['id']},
                body={
                    'cards': []
                })
        )
        game: StartedGame = read_response_body(resp.get_body())

        self.assertEqual(RoundStatus.TRICKS.name, game['status'])

        # ask for a suggestion so we know what card we can play
        resp = suggestion.main(
            build_request(
                route_params={'game_id': created_game['id']})
        )
        suggested_play: PlaySuggestion = read_response_body(resp.get_body())

        # play
        resp = play.main(
            build_request(
                route_params={'game_id': created_game['id']},
                body={
                    'card': suggested_play['card']
                })
        )
        game: StartedGame = read_response_body(resp.get_body())

        self.assertEqual(RoundStatus.TRICKS.name, game['status'])
        self.assertEqual(2, len(game['round']['tricks']))

    def test_prepass_and_rescind_prepass(self):
        '''A non-active player can prepass and rescind that prepass'''
        game: StartedGame = self.get_initial_game()

        non_active_player = next(
            p for p in game['round']['players']
            if game['round']['active_player'] and p['identifier'] !=
            game['round']['active_player']['identifier'])

        # prepass
        resp = bid.main(
            build_request(
                route_params={'game_id': game['id']},
                headers={'x-ms-client-principal-id': non_active_player['identifier']},
                body={
                    'amount': BidAmount.PASS
                })
        )
        game: StartedGame = read_response_body(resp.get_body())
        non_active_player = next(p for p in game['round']
                                 ['players'] if p['identifier'] == non_active_player['identifier'])
        self.assertTrue(non_active_player['prepassed'])

        # rescind prepass
        resp = rescind_prepass.main(
            build_request(
                route_params={'game_id': game['id']},
                headers={'x-ms-client-principal-id': non_active_player['identifier']},
            )
        )
        game: StartedGame = read_response_body(resp.get_body())
        non_active_player = next(p for p in game['round']
                                 ['players'] if p['identifier'] == non_active_player['identifier'])
        self.assertFalse(non_active_player['prepassed'])
