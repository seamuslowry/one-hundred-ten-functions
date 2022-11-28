'''Facilitate interaction with rounds in the DB'''

from app.models import (Bid, BidAmount, Deck, DetailedDiscard, Group, Round,
                        RoundStatus, SelectableSuit, SelectTrump)
from app.services import card, person, trick


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


def from_db(game_round: dict) -> Round:
    '''Convert the provided dict from the DB into a Round instance'''
    trump_name = game_round['trump']
    trump = SelectableSuit[trump_name] if trump_name else None

    model_round = Round(
        players=Group(list(map(person.player_from_db, game_round['players']))),
        bids=list(map(__bid_from_db, game_round['bids'])),
        deck=__deck_from_db(game_round['deck']),
        discards=list(map(__discard_from_db, game_round['discards'])),
        tricks=list(map(trick.from_db, game_round['tricks']))
    )

    # set selction of trump using round's computation of bidder
    active_bidder = model_round.active_bidder
    model_round.selection = SelectTrump(active_bidder.identifier,
                                        trump) if (active_bidder and trump) else None

    return model_round


def __deck_to_db(deck: Deck) -> dict:
    '''Convert the provided deck into the dict structure used by the DB'''
    return {
        'seed': deck.seed,
        'pulled': deck.pulled
    }


def __deck_from_db(deck: dict) -> Deck:
    '''Convert the provided dict from the DB into a Deck instance'''
    return Deck(
        seed=deck['seed'],
        pulled=deck['pulled']
    )


def __bid_to_db(bid: Bid) -> dict:
    '''Convert the provided bid into the dict structure used by the DB'''
    return {
        'identifier': bid.identifier,
        'amount': bid.amount.value
    }


def __bid_from_db(bid: dict) -> Bid:
    '''Convert the provided dict from the DB into a Bid instance'''
    return Bid(
        identifier=bid['identifier'],
        amount=BidAmount(bid['amount'])
    )


def __discard_to_db(discard: DetailedDiscard) -> dict:
    '''Convert the provided discard into the dict structure used by the DB'''
    return {
        'identifier': discard.identifier,
        'cards': list(map(card.to_db, discard.cards)),
        'kept':  list(map(card.to_db, discard.kept))
    }


def __discard_from_db(discard: dict) -> DetailedDiscard:
    '''Convert the provided dict from the DB into a Discard instance'''
    return DetailedDiscard(
        identifier=discard['identifier'],
        cards=list(map(card.from_db, discard['cards'])),
        kept=list(map(card.from_db, discard['kept']))
    )


def json(game_round: Round, client: str) -> dict:
    '''Convert the provided round into the structure it should provide the client'''

    non_zero_bids = [bid for bid in game_round.bids if bid.amount > 0]
    current_bid = non_zero_bids[-1] if non_zero_bids else Bid('', BidAmount.PASS)
    bidder = game_round.players.by_identifier(current_bid.identifier)

    return {
        'players': list(map(lambda p: person.json(p, client), game_round.players)),
        'dealer': person.json(game_round.dealer),
        'bidder': person.json(bidder) if bidder else None,
        'bid': current_bid.amount.name if current_bid.amount else None,
        'trump': game_round.trump.name if game_round.trump else None,
        'tricks': list(map(trick.json, game_round.tricks)),
        # only active rounds have active players
        'active_player': (
            person.json(game_round.active_player)
            if game_round.status not in [
                RoundStatus.COMPLETED_NO_BIDDERS,
                RoundStatus.COMPLETED
            ]
            else None)
    }
