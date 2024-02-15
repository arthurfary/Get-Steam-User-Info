from flask import Flask, jsonify

from SteamRoutesBlueprint import steam_games_bp

app = Flask(__name__)
app.register_blueprint(steam_games_bp)