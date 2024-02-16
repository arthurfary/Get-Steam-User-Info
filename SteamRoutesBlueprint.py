from flask import Blueprint
from cache import cache
from modules.SteamGameRequests import SteamGameRequests

steam_games_bp = Blueprint('steam', __name__)

@steam_games_bp.route("/games/getAppidNamePair")
def get_appid_name_pair():
    return SteamGameRequests.get_appid_name_pair()

@steam_games_bp.route("/games/<steamId>", methods=["GET"])
@cache.cached()
def get_user_owned_games(steamId):
    return SteamGameRequests.get_user_owned_games(steamId)

@steam_games_bp.route("/recent/<steamId>", methods=["GET"])
@cache.cached()
def get_recently_played_games(steamId):
    return SteamGameRequests.get_recently_played_games(steamId)

@steam_games_bp.route("/games/fromurl/<vanityUrl>", methods=["GET"])
@cache.cached()
def get_user_owned_games_from_vanity_url(vanityUrl):
    return SteamGameRequests.get_user_owned_games_from_vanity_url(vanityUrl)