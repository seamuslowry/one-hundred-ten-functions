'''Retrieve Info unit tests'''
from time import time
from unittest import TestCase

import events
import game_info
import join_game
import players
import search_games
from app.dtos.client import CompletedGame, Event, User, WaitingGame
from app.mappers.constants import EventType
from tests.helpers import (build_request, completed_game, lobby_game,
                           read_response_body)


class TestRetrieveInfo(TestCase):
    '''Unit tests to the client can query for info as necessary'''

    def test_search_winner(self):
        '''Can search by winner'''
        game: CompletedGame = completed_game()

        # search games
        resp = search_games.main(
            build_request(
                body={
                    'winner': game['winner']['identifier']
                })
        )
        games = read_response_body(resp.get_body())
        self.assertIn(game['id'], list(map(lambda g: g['id'], games)))

    def test_game_info(self):
        '''Can retrieve information about a game'''
        original_game: CompletedGame = completed_game()

        # get that game's info
        resp = game_info.main(
            build_request(
                route_params={'game_id': original_game['id']})
        )
        game = read_response_body(resp.get_body())
        self.assertEqual(game['id'], original_game['id'])

    def test_game_events(self):
        '''Can retrieve event information about a game'''
        original_game: CompletedGame = completed_game()

        # get that game's events
        resp = events.main(
            build_request(
                route_params={'game_id': original_game['id']})
        )
        retrieved_events: list[Event] = read_response_body(resp.get_body())
        self.assertIsNotNone(original_game['results'])
        assert original_game['results']
        self.assertNotEqual(original_game['results'], [])
        self.assertGreaterEqual(len(retrieved_events), len(original_game['results']))
        self.assertEqual(
            retrieved_events[len(retrieved_events)-len(original_game['results']):],
            original_game['results'])
        self.assertEqual(retrieved_events[-1]['type'], EventType.GAME_END.name)

    def test_game_players(self):
        '''Can retrieve user information for players on a game'''
        original_game: WaitingGame = lobby_game()
        other_players = list(map(lambda i: f'{time()}-{i}', range(1, 4)))
        for player in other_players:
            join_game.main(
                build_request(
                    route_params={'game_id': original_game['id']},
                    headers={'x-ms-client-principal-id': player}))

        # get that game's players
        resp = players.main(
            build_request(
                route_params={'game_id': original_game['id']})
        )
        retrieved_users: list[User] = read_response_body(resp.get_body())
        self.assertEqual(4, len(retrieved_users))
        self.assertEqual(
            [original_game['organizer']['identifier']] + other_players,
            list(map(lambda p: p['identifier'],
                     retrieved_users)))

    def test_search_users(self):
        '''Can retrieve user information by substring of name'''
        original_game: WaitingGame = lobby_game()
        other_players = list(map(lambda i: f'{time()}-{i}', range(1, 4)))
        for player in other_players:
            join_game.main(
                build_request(
                    route_params={'game_id': original_game['id']},
                    headers={'x-ms-client-principal-id': player}))

        # get that game's players
        resp = players.main(
            build_request(
                route_params={'game_id': original_game['id']})
        )
        retrieved_users: list[User] = read_response_body(resp.get_body())
        self.assertEqual(4, len(retrieved_users))
        self.assertEqual(
            [original_game['organizer']['identifier']] + other_players,
            list(map(lambda p: p['identifier'],
                     retrieved_users)))
