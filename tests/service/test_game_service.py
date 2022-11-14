'''Game Service unit tests'''
from unittest import TestCase

from hundredandten import HundredAndTen

from service import GameService


class TestGameService(TestCase):
    '''Unit tests to ensure game translations work as expected'''

    def test_game_conversion(self):
        '''HundredAndTen can be converted to and from a DB save'''
        initial_game = HundredAndTen(seed='test_game')

        self.assertEqual(initial_game, GameService.from_db(GameService.to_db(initial_game)))
