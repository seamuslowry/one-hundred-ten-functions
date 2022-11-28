'''Init the decorators module'''
from app.decorators.errors.error_aggregation import handle_error as catcher
from app.decorators.requests.authorized_user import parse_user
from app.decorators.requests.specified_game import parse_game
