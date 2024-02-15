from flask import Flask
from markupsafe import escape
import requests
import os

from dotenv import load_dotenv
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

app = Flask(__name__)

def make_steam_request(endpoint, params):
    base_url = f"https://api.steampowered.com/{endpoint}"
    params["key"] = STEAM_API_KEY
    params["format"] = "json"
    response = requests.get(base_url, params=params)
    return response.json()

@app.route("/games/getAllSteamGames/", methods=["GET"])
def get_all_steam_games():
    data = make_steam_request("ISteamApps/GetAppList/v2", {})
    return data['applist']['apps']

@app.route("/games/<steamId>", methods=["GET"])
def get_steam_games(steamId):
    response = make_steam_request("IPlayerService/GetOwnedGames/v0001", {"steamId": escape(steamId)})
    steam_games = get_all_steam_games()

    for count, user_game in enumerate(response['response']['games']):
        for steam_game in steam_games: 
            if user_game['appid'] == steam_game['appid']:
                response['response']['games'][count]['name'] = steam_game['name']
                
    return response

@app.route("/recent/<steamId>", methods=["GET"])
def get_last_two_weeks_played(steamId):
    response = make_steam_request("IPlayerService/GetRecentlyPlayedGames/v0001", {"steamId": escape(steamId)})
    return response

@app.route("/games/fromurl/<vanityUrl>", methods=["GET"])
def get_steam_user_data_from_url(vanityUrl):
    data = make_steam_request("ISteamUser/ResolveVanityURL/v1", {"vanityurl": escape(vanityUrl)})
    steamid = data['response']['steamid']
    return get_steam_games(steamid)
