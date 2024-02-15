from flask import Flask, jsonify
import requests
import os
from markupsafe import escape
from dotenv import load_dotenv
from SteamGames import SteamGames

load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_GAMES = SteamGames()

app = Flask(__name__)

def make_steam_request(endpoint, params):
    base_url = f"https://api.steampowered.com/{endpoint}"
    params["key"] = STEAM_API_KEY
    params["format"] = "json"
    response = requests.get(base_url, params=params)
    return response.json()

@app.route("/games/<steamId>", methods=["GET"])
def get_user_owned_games(steamId):
    owned_games = make_steam_request("IPlayerService/GetOwnedGames/v0001", {"steamId": escape(steamId)})['response']
    steam_games = STEAM_GAMES.get_games()

    for count, user_game in enumerate(owned_games['games']):
        if user_game['appid'] in steam_games:
            owned_games['games'][count]['name'] = steam_games[user_game['appid']]
                
    return jsonify(owned_games)

@app.route("/recent/<steamId>", methods=["GET"])
def get_recently_played_games(steamId):
    recent_games = make_steam_request("IPlayerService/GetRecentlyPlayedGames/v0001", {"steamId": escape(steamId)})
    return jsonify(recent_games)

@app.route("/games/fromurl/<vanityUrl>", methods=["GET"])
def get_user_owned_games_from_vanity_url(vanityUrl):
    data = make_steam_request("ISteamUser/ResolveVanityURL/v1", {"vanityurl": escape(vanityUrl)})
    steamid = data['response']['steamid']
    return get_user_owned_games(steamid)
