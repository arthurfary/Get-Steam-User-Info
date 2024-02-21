from flask import Blueprint, jsonify

from cache import cache
from ..SteamRequest import SteamRequest

from .SteamUserRequests import SteamUserRequests

steam_users_bp = Blueprint('steam_users', __name__)
user_requests = SteamUserRequests()

@steam_users_bp.route("/users/<id_or_url>", methods=["GET"])
@cache.cached()
@SteamRequest.resolve_steam_id_and_handle_error
def get_user_summary(steam_id):
    return user_requests.get_user_summary(steam_id)

@steam_users_bp.route("/users/friends/<id_or_url>", methods=["GET"])
@cache.cached()
@SteamRequest.resolve_steam_id_and_handle_error
def get_user_friends(steam_id):
    return user_requests.get_user_friends(steam_id)


