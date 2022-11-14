'''Round Service unit tests'''
from unittest import TestCase

from hundredandten.actions import Bid, Discard
from hundredandten.constants import BidAmount, SelectableSuit
from hundredandten.deck import Deck
from hundredandten.group import Group, Player
from hundredandten.round import Round
from hundredandten.trick import Trick

from service import round as RoundService


class TestRoundService(TestCase):
    '''Unit tests to ensure round translations work as expected'''

    def test_blank_round_to_db(self):
        '''Initial round can be converted for DB save'''
        self.assertIsNotNone(RoundService.to_db(
            Round()))

    def test_no_trump_round_to_db(self):
        '''Round in bidding can be converted for DB save'''
        self.assertIsNotNone(RoundService.to_db(
            Round(
                players=Group([Player('')]),
                bids=[Bid('', BidAmount.PASS)],
                deck=Deck()
            )))

    def test_trump_round_to_db(self):
        '''Round in discard can be converted for DB save'''
        self.assertIsNotNone(RoundService.to_db(
            Round(
                players=Group([Player('')]),
                bids=[Bid('', BidAmount.PASS)],
                deck=Deck(),
                trump=SelectableSuit.CLUBS
            )))

    def test_discard_round_to_db(self):
        '''Round discarding can be converted for DB save'''
        self.assertIsNotNone(RoundService.to_db(
            Round(
                players=Group([Player('')]),
                bids=[Bid('', BidAmount.PASS)],
                deck=Deck(),
                trump=SelectableSuit.CLUBS,
                discards=[Discard('', [])]
            )))

    def test_tricks_round_to_db(self):
        '''Round playing tricks can be converted for DB save'''
        self.assertIsNotNone(RoundService.to_db(
            Round(
                players=Group([Player('')]),
                bids=[Bid('', BidAmount.PASS)],
                deck=Deck(),
                trump=SelectableSuit.CLUBS,
                discards=[Discard('', [])],
                tricks=[Trick(SelectableSuit.CLUBS, [])]
            )))

    def test_blank_round_from_db(self):
        '''Initial round can be converted from DB save'''
        self.assertIsNotNone(RoundService.from_db(RoundService.to_db(
            Round())))

    def test_no_trump_round_from_db(self):
        '''Round in bidding can be converted from DB save'''
        self.assertIsNotNone(RoundService.from_db(RoundService.to_db(
            Round(
                players=Group([Player('')]),
                bids=[Bid('', BidAmount.PASS)],
                deck=Deck()
            ))))

    def test_trump_round_from_db(self):
        '''Round in discard can be converted from DB save'''
        self.assertIsNotNone(RoundService.from_db(RoundService.to_db(
            Round(
                players=Group([Player('')]),
                bids=[Bid('', BidAmount.PASS)],
                deck=Deck(),
                trump=SelectableSuit.CLUBS
            ))))

    def test_discard_round_from_db(self):
        '''Round discarding can be converted from DB save'''
        self.assertIsNotNone(RoundService.from_db(RoundService.to_db(
            Round(
                players=Group([Player('')]),
                bids=[Bid('', BidAmount.PASS)],
                deck=Deck(),
                trump=SelectableSuit.CLUBS,
                discards=[Discard('', [])]
            ))))

    def test_tricks_round_from_db(self):
        '''Round playing tricks can be converted from DB save'''
        self.assertIsNotNone(RoundService.from_db(RoundService.to_db(
            Round(
                players=Group([Player('')]),
                bids=[Bid('', BidAmount.PASS)],
                deck=Deck(),
                trump=SelectableSuit.CLUBS,
                discards=[Discard('', [])],
                tricks=[Trick(SelectableSuit.CLUBS, [])]
            ))))
