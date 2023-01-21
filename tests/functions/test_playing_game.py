'''Playing Game unit tests'''
from unittest import TestCase

import bid
import discard
import leave_game
import play
import rescind_prepass
import select_trump
import suggestion
from app.dtos.client import CompletedGame, PlaySuggestion, StartedGame
from app.models import BidAmount, RoundStatus, SelectableSuit
from tests.helpers import build_request, read_response_body, started_game


class TestPlayingGame(TestCase):
    '''Unit tests to ensure games that are in progress behave as expected'''

    def test_perform_round_actions(self):
        '''A round of the game can be played'''
        created_game: StartedGame = started_game()
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
        game: StartedGame = started_game()

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

    def test_leave_playing_game(self):
        '''A player can leave an active game by automating themselves'''
        original_game: StartedGame = started_game()
        active_player = original_game['round']['active_player']
        assert active_player
        self.assertFalse(active_player['automate'])

        # leave
        resp = leave_game.main(
            build_request(
                route_params={'game_id': original_game['id']}
            )
        )
        game: CompletedGame = read_response_body(resp.get_body())
        active_player = next(p for p in game['players']
                             if p['identifier'] == active_player['identifier'])

        self.assertTrue(active_player['automate'])
