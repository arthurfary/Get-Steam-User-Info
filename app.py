from flask import Flask
from cache import cache
from werkzeug.exceptions import BadRequest

from modules.HomeBlueprint import home_bp
from modules.games.SteamGamesRoutesBlueprint import steam_games_bp
from modules.user.SteamUserRoutes import steam_users_bp

app = Flask(__name__)

cache.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(steam_games_bp)
app.register_blueprint(steam_users_bp)


@app.errorhandler(BadRequest)
def handle_bad_request(e: BadRequest):
    return e.description, 400


