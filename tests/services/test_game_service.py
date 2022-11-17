'''Game Service unit tests'''
from unittest import TestCase

from models import Game, Group, Player, Round, RoundRole
from services import GameService
from services.cosmos import game_client


class TestGameService(TestCase):
    '''Unit tests to ensure game translations work as expected'''

    def test_game_conversion(self):
        '''Game can be converted to and from a DB save'''
        initial_game = Game(id='test', seed='test_game')

        self.assertEqual(initial_game, GameService.from_db(GameService.to_db(initial_game)))

    def test_game_conversion_partitions_waiting(self):
        '''Game converts status to the name when waiting for players'''
        initial_game = Game(id='test', seed='test_game')

        self.assertEqual(initial_game.status.name,
                         GameService.to_db(initial_game).get('status', ''))

    def test_game_conversion_partitions_playing(self):
        '''Game converts status to generic playing when in rounds'''
        initial_game = Game(id='test', seed='test_game', rounds=[Round(
            players=Group([Player(identifier='', roles={RoundRole.DEALER})]))])

        self.assertNotEqual(initial_game.status.name,
                            GameService.to_db(initial_game).get('status', ''))

    def test_game_client_conversion(self):
        '''Game can be converted to client json'''
        initial_game = Game(id='test', seed='test_game', rounds=[Round(
            players=Group([Player(identifier='', roles={RoundRole.DEALER})]))])

        self.assertIsNotNone(GameService.json(initial_game, ''))

    def test_game_save(self):
        '''Game can be saved to the DB'''
        game = Game(id='test', seed='test_game')

        game_client.upsert_item.return_value = GameService.to_db(game)

        self.assertIsNotNone(GameService.save(game))
        game_client.upsert_item.assert_called_once()
