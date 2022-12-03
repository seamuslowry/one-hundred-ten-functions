'''Facilitate interaction with the game DB'''
from typing import Optional

from app.models import Accessibility, Game, GameRole, GameStatus, Group
from app.services import event, person
from app.services import round as round_service
from app.services.cosmos import game_client


def save(game: Game) -> Game:
    '''Save the provided game to the DB'''
    return from_db(game_client.upsert_item(to_db(game)))


def get(game_id: str) -> Game:
    '''Retrieve the game with the provided ID'''
    return from_db(game_client.read_item(game_id, game_id))


def to_db(game: Game) -> dict:
    '''Convert the provided game into the dict structure used by the DB'''
    return {
        'id': game.id,
        'status': game.status.name,
        'name': game.name,
        'seed': game.seed,
        'accessibility': game.accessibility.name,
        'people': list(map(person.to_db, game.people)),
        'rounds': list(map(round_service.to_db, game.rounds)),
        **__computed_properties(game)
    }


def from_db(game: dict) -> Game:
    '''Convert the provided dict from the DB into a Game instance'''
    return Game(
        id=game['id'],
        name=game['name'],
        seed=game['seed'],
        accessibility=Accessibility[game['accessibility']],
        people=Group(list(map(person.person_from_db, game['people']))),
        rounds=list(map(round_service.from_db, game['rounds']))
    )


def __json(game: Game, client: str) -> dict:
    '''Convert the provided game into the structure it should provide the client'''

    return {
        'id': game.id,
        'name': game.name,
        'status': game.status.name,
        # properties that are only relevant while waiting for the game to begin
        **(__waiting_game_properties(game)
           if game.status == GameStatus.WAITING_FOR_PLAYERS
           # properties that are only relevant once the game has begun
           else __started_game_properties(game, client))
    }


def json(game: Game, client: str, initial_event_knowledge: Optional[int] = None) -> dict:
    '''
    Convert the provided game client information
    and provide information on events since on initial event
    '''

    return {
        **__json(game, client),
        # only send up the results if requested
        **({'results': event.json(game.events[initial_event_knowledge:], client)}
           if initial_event_knowledge is not None else {})
    }


def search_waiting(
        text: str,
        max_count: int,
        client: str,
        roles: Optional[list[GameRole]] = None) -> list[Game]:
    '''Retrieve the games the provided client can access that are waiting for players'''
    if roles:
        return __search_waiting_by_role(text, max_count, client, roles)
    return __search_waiting_without_client(text, max_count, client)


def search_playing(
        text: str,
        max_count: int,
        client: str,
        active: bool) -> list[Game]:
    '''
    Retrieve games that are playing rounds the client is a player on
    If active is True, will only return games where it is the client's turn to play
    '''
    if active:
        return __search_playing_by_active(text, max_count, client)
    return __search_playing_by_text(text, max_count, client)


def __search_playing_by_active(
        text: str,
        max_count: int,
        client: str) -> list[Game]:
    '''Retrieve games where it is the client's turn to play'''
    return list(map(from_db, game_client.query_items(
        ('select * from game '
         'where not array_contains(@statuses, game.status) '
         'and contains(lower(game.name), lower(@text)) '
         'and game.activePlayer = @client '
         'order by game.name '
         'offset 0 limit @max'),
        parameters=[
            {
                'name': '@statuses',
                'value': [GameStatus.WAITING_FOR_PLAYERS.name, GameStatus.WON.name]
            },
            {'name': '@text', 'value': text},
            {'name': '@client', 'value': client},
            {'name': '@max', 'value': max_count}
        ],
        enable_cross_partition_query=True
    )))


def __search_playing_by_text(
        text: str,
        max_count: int,
        client: str) -> list[Game]:
    '''Retrieve games playing rounds where the client is a player'''
    return list(map(from_db, game_client.query_items(
        ('select * from game '
         'where not array_contains(@statuses, game.status) '
         'and contains(lower(game.name), lower(@text)) '
         'and exists(select value person from person in game.people '
         'where person.identifier = @client '
         'and array_contains(person.roles, @role)) '
         'order by game.name '
         'offset 0 limit @max'),
        parameters=[
            {
                'name': '@statuses',
                'value': [GameStatus.WAITING_FOR_PLAYERS.name, GameStatus.WON.name]
            },
            {'name': '@text', 'value': text},
            {'name': '@client', 'value': client},
            {'name': '@role', 'value': GameRole.PLAYER.name},
            {'name': '@max', 'value': max_count}
        ],
        enable_cross_partition_query=True
    )))


def __search_waiting_without_client(
        text: str, max_count: int, client: str) -> list[Game]:
    '''Retrieve the accessible games the client is not on that are waiting for players'''
    return list(map(from_db, game_client.query_items(
        ('select * from game '
         'where game.status = @status '
         'and game.accessibility = @accessibility '
         'and contains(lower(game.name), lower(@text)) '
         'and not array_contains(game.people, {"identifier": @client}, true) '
         'order by game.name '
         'offset 0 limit @max'),
        parameters=[
            {'name': '@status', 'value': GameStatus.WAITING_FOR_PLAYERS.name},
            {'name': '@accessibility', 'value': Accessibility.PUBLIC.name},
            {'name': '@text', 'value': text},
            {'name': '@client', 'value': client},
            {'name': '@max', 'value': max_count}
        ],
        enable_cross_partition_query=True
    )))


def __search_waiting_by_role(
        text: str, max_count: int, client: str, roles: list[GameRole]) -> list[Game]:
    '''
    Retrieve the games the provided client is on that are waiting for players
    '''
    return list(map(from_db, game_client.query_items(
        ('select * from game '
         'where game.status = @status '
         'and contains(lower(game.name), lower(@text)) '
         'and exists(select value person from person in game.people '
         'where person.identifier = @client '
         'and exists(select value role from role in person.roles '
         'where array_contains(@roles, role))) '
         'order by game.name '
         'offset 0 limit @max'),
        parameters=[
            {'name': '@status', 'value': GameStatus.WAITING_FOR_PLAYERS.name},
            {'name': '@text', 'value': text},
            {'name': '@client', 'value': client},
            {
                'name': '@roles',
                'value': list(map(lambda r: r.name, roles))
            },
            {'name': '@max', 'value': max_count}
        ],
        enable_cross_partition_query=True
    )))


def __waiting_game_properties(game: Game) -> dict:
    return {
        'accessibility': game.accessibility.name,
        'organizer': person.json(game.organizer),
        'players': list(map(person.json, [p for p in game.players if p != game.organizer])),
        'invitees': list(map(person.json, [p for p in game.invitees if p not in game.players]))
    }


def __started_game_properties(game: Game, client: str) -> dict:
    return {
        'round': round_service.json(game.active_round, client),
        'scores': game.scores
    }


def __computed_properties(game: Game) -> dict:
    '''Properties added to the DB for searching; will not be read back from the DB'''
    return {
        'activePlayer': game.active_round.active_player.identifier if game.rounds else None,
        'winner': game.winner.identifier if game.winner else None
    }
