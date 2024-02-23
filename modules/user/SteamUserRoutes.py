from flask import Blueprint, jsonify

from cache import cache
from ..SteamRequest import SteamRequest

from .SteamUserRequests import SteamUserRequests

steam_users_bp = Blueprint('steam_users', __name__)
user_requests = SteamUserRequests()

@steam_users_bp.route("/users/<id_or_url>", methods=["GET"])
@cache.cached()
def get_user_summary(id_or_url):
    steam_id = SteamRequest.resolve_steam_id(id_or_url)
    return user_requests.get_user_summary(steam_id)

@steam_users_bp.route("/users/friends/<id_or_url>", methods=["GET"])
@cache.cached()
def get_user_friends(id_or_url):
    steam_id = SteamRequest.resolve_steam_id(id_or_url)
    return user_requests.get_user_friends(steam_id)

@steam_users_bp.route("/users/achievements/<id_or_url>/<game_id>", methods=["GET"])
@cache.cached()
def get_user_achievements(id_or_url, game_id):
    steam_id = SteamRequest.resolve_steam_id(id_or_url)
    return user_requests.get_user_achievements(steam_id, game_id)