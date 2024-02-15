from modules.SteamGames import SteamGames
from modules.SteamRequest import SteamRequest

from flask import jsonify
from markupsafe import escape

class SteamGameRequests(SteamRequest):

    @staticmethod
    def get_appid_name_pair():
        return SteamGames.get_games()

    @staticmethod
    def get_user_owned_games(steamId):
        owned_games = SteamRequest.make_steam_request("IPlayerService/GetOwnedGames/v0001", {"steamId": escape(steamId)})['response']
        steam_games = SteamGames.get_games()

        for count, user_game in enumerate(owned_games['games']):
            if user_game['appid'] in steam_games:
                owned_games['games'][count]['name'] = steam_games[user_game['appid']]
                
        return jsonify(owned_games)

    @staticmethod
    def get_recently_played_games(steamId):
        recent_games = SteamRequest.make_steam_request("IPlayerService/GetRecentlyPlayedGames/v0001", {"steamId": escape(steamId)})
        return jsonify(recent_games)

    @staticmethod
    def get_user_owned_games_from_vanity_url(vanityUrl):
        data = SteamRequest.make_steam_request("ISteamUser/ResolveVanityURL/v1", {"vanityurl": escape(vanityUrl)})
        steamid = data['response']['steamid']
        return SteamGameRequests.get_user_owned_games(steamid)
