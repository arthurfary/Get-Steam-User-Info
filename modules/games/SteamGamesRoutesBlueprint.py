from flask import Blueprint

from .SteamGameRequests import SteamGameRequests
from cache import cache
from ..SteamRequest import SteamRequest 

steam_games_bp = Blueprint('steam', __name__)
game_requests = SteamGameRequests()

@steam_games_bp.route("/games/getAppidNamePair")
def get_appid_name_pair():
    return game_requests.get_appid_name_pair()

@steam_games_bp.route("/games/<id_or_url>", methods=["GET"])
@cache.cached()
@SteamRequest.resolve_steam_id
def get_user_owned_games(id):
    return game_requests.get_user_owned_games(id)

@steam_games_bp.route("/games/recent/<id_or_url>", methods=["GET"])
@cache.cached()
@SteamRequest.resolve_steam_id
def get_recently_played_games(id):
    return game_requests.get_recently_played_games(id)

@steam_games_bp.route("/games/gameinfo/<id_or_url>/<game_id>", methods=["GET"])
@cache.cached()
@SteamRequest.resolve_steam_id
def get_specific_game_info(id, game_id):
    return game_requests.get_specific_game_info(id, game_id)

