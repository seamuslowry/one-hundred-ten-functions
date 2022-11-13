'''Facilitate interaction with rounds in the DB'''

from hundredandten.actions import Bid, Discard
from hundredandten.deck import Deck
from hundredandten.round import Round

from service import card, person, trick


def to_db(game_round: Round) -> dict:
    '''Convert the provided round into the dict structure used by the DB'''
    return {
        'players': list(map(person.to_db, game_round.players)),
        'bids': list(map(__bid_to_db, game_round.bids)),
        'deck': __deck_to_db(game_round.deck),
        'trump': game_round.trump.name if game_round.trump else None,
        'discards': list(map(__discard_to_db, game_round.discards)),
        'tricks': list(map(trick.to_db, game_round.tricks))
    }


def __deck_to_db(deck: Deck) -> dict:
    '''Convert the provided deck into the dict structure used by the DB'''
    return {
        'seed': deck.seed,
        'pulled': deck.pulled
    }


def __bid_to_db(bid: Bid) -> dict:
    '''Convert the provided bid into the dict structure used by the DB'''
    return {
        'identifier': bid.identifier,
        'amount': bid.amount.value
    }


def __discard_to_db(discard: Discard) -> dict:
    '''Convert the provided discard into the dict structure used by the DB'''
    return {
        'identifier': discard.identifier,
        'discards': list(map(card.to_db, discard.cards))
    }
