from flask import Flask, jsonify
from cache import cache

from modules.HomeBlueprint import home_bp
from modules.games.SteamGamesRoutesBlueprint import steam_games_bp

app = Flask(__name__)

cache.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(steam_games_bp)