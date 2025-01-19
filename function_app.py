'''
Main entrypoint for app
'''
import azure.functions as func
from create_game import bp as create_game_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app.register_functions(create_game_bp)
