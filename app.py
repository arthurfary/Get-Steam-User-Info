from flask import Flask, jsonify
from cache import cache

from SteamRoutesBlueprint import steam_games_bp

app = Flask(__name__)

cache.init_app(app)

app.register_blueprint(steam_games_bp)