'''Game Service unit tests'''
from unittest import TestCase

from hundredandten import HundredAndTen

from service import GameService


class TestGameService(TestCase):
    '''Unit tests to ensure game translations work as expected'''

    def test_game_to_db(self):
        '''HundredAndTen can be converted for DB save'''
        self.assertIsNotNone(GameService.to_db(HundredAndTen()))

    def test_game_from_db(self):
        '''HundredAndTen can be converted from DB save'''
        initial_game = HundredAndTen(seed='test_game')

        self.assertEqual(initial_game, GameService.from_db(GameService.to_db(initial_game)))
