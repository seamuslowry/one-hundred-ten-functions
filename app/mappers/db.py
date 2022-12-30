'''A module to convert DB DTOs to models and vice versa'''
from functools import singledispatch

from app import models
from app.dtos import db


@singledispatch
def convert(obj):
    '''Convert the provided object to its corresponding DTO / model'''
    return obj


@convert.register
def _(card: models.Card) -> db.Card:
    return db.Card(
        suit=card.suit.name,
        number=card.number.name
    )


@convert.register
def _(card: db.Card) -> models.Card:
    suit = None

    try:
        suit = models.SelectableSuit[card['suit']]
    except KeyError:
        pass

    try:
        suit = models.UnselectableSuit[card['suit']]
    except KeyError:
        pass

    assert suit

    return models.Card(
        suit=suit,
        number=models.CardNumber[card['number']]
    )


@convert.register
def _(person: models.Person) -> db.Person:
    return db.Person(
        id=person.identifier,
        roles=list(map(lambda r: r.name, person.roles)),
        automate=person.automate
    )


@convert.register
def _(person: db.Person) -> models.Person:
    return models.Person(
        identifier=person['id'],
        automate=person['automate'],
        roles=set(map(lambda r: models.RoundRole[r], person['roles']))
    )


@convert.register
def _(player: models.Player) -> db.Player:
    return db.Player(
        id=player.identifier,
        roles=list(map(lambda r: r.name, player.roles)),
        automate=player.automate,
        hand=list(map(convert, player.hand))
    )


@convert.register
def _(player: db.Player) -> models.Player:
    return models.Player(
        identifier=player['id'],
        automate=player['automate'],
        roles=set(map(lambda r: models.RoundRole[r], player['roles'])),
        hand=list(map(convert, player['hand']))
    )


@convert.register
def _(bid: models.Bid) -> db.Bid:
    return db.Bid(
        identifier=bid.identifier,
        amount=bid.amount.value
    )


@convert.register
def _(bid: db.Bid) -> models.Bid:
    return models.Bid(
        identifier=bid['identifier'],
        amount=models.BidAmount(bid['amount'])
    )


@convert.register
def _(deck: models.Deck) -> db.Deck:
    return db.Deck(
        seed=deck.seed,
        pulled=deck.pulled
    )


@convert.register
def _(deck: db.Deck) -> models.Deck:
    return models.Deck(
        seed=deck['seed'],
        pulled=deck['pulled']
    )


@convert.register
def _(discard: models.DetailedDiscard) -> db.Discard:
    return db.Discard(
        identifier=discard.identifier,
        cards=list(map(convert, discard.cards)),
        kept=list(map(convert, discard.kept))
    )


@convert.register
def _(discard: db.Discard) -> models.DetailedDiscard:
    return models.DetailedDiscard(
        identifier=discard['identifier'],
        cards=list(map(convert, discard['cards'])),
        kept=list(map(convert, discard['kept']))
    )


@convert.register
def _(play: models.Play) -> db.Play:
    return db.Play(
        identifier=play.identifier,
        card=convert(play.card)
    )


@convert.register
def _(play: db.Play) -> models.Play:
    return models.Play(
        identifier=play['identifier'],
        card=convert(play['card'])
    )


@convert.register
def _(trick: models.Trick) -> db.Trick:
    return db.Trick(
        plays=list(map(convert, trick.plays)),
        round_trump=trick.round_trump.name
    )


@convert.register
def _(trick: db.Trick) -> models.Trick:
    return models.Trick(
        plays=list(map(convert, trick['plays'])),
        round_trump=models.SelectableSuit[trick['round_trump']]
    )


@convert.register
def _(m_round: models.Round) -> db.Round:
    return db.Round(
        players=list(map(convert, m_round.players)),
        bids=list(map(convert, m_round.bids)),
        deck=convert(m_round.deck),
        trump=m_round.trump.name if m_round.trump else None,
        discards=list(map(convert, m_round.discards)),
        tricks=list(map(convert, m_round.tricks))
    )


@convert.register
def _(db_round: db.Round) -> models.Round:

    trump_name = db_round['trump']
    trump = models.SelectableSuit[trump_name] if trump_name else None

    model_round = models.Round(
        players=models.Group(map(convert, db_round['players'])),
        bids=list(map(convert, db_round['bids'])),
        deck=convert(db_round['deck']),
        discards=list(map(convert, db_round['discards'])),
        tricks=list(map(convert, db_round['tricks']))
    )

    active_bidder = model_round.active_bidder
    model_round.selection = models.SelectTrump(active_bidder.identifier,
                                               trump) if (active_bidder and trump) else None

    return model_round


@convert.register
def _(game: models.Game) -> db.Game:
    winner = game.winner
    active_player = game.active_round.active_player if game.rounds and not winner else None

    return db.Game(
        id=game.id,
        status=game.status.name,
        name=game.name,
        seed=game.seed,
        accessibility=game.accessibility.name,
        people=list(map(convert, game.people)),
        rounds=[],
        active_player=active_player.identifier if active_player else None,
        winner=winner.identifier if winner else None
    )


@convert.register
def _(game: db.Game) -> models.Game:
    return models.Game(
        id=game['id'],
        name=game['name'],
        seed=game['seed'],
        accessibility=models.Accessibility[game['accessibility']],
        people=models.Group(map(convert, game['people'])),
        rounds=list(map(convert, game['rounds'])))
