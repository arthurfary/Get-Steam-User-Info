from ..SteamRequest import SteamRequest

from flask import jsonify
from markupsafe import escape

class SteamGameRequests(SteamRequest):
    steam_games = None
    owned_games = None

    def get_steam_games(self):
        if self.steam_games == None:
            data = SteamRequest.make_steam_request("ISteamApps/GetAppList/v2", {})
            all_games = data['applist']['apps']
            appid_game_pair = {game['appid']: game['name'] for game in all_games}
            self.steam_games = appid_game_pair
        return self.steam_games

    def get_owned_games(self, steamId):
        if self.owned_games == None:
            data = SteamRequest.make_steam_request("IPlayerService/GetOwnedGames/v0001", {"steamId": escape(steamId)})['response']['games']
            appid_keyed_dict = {
                game['appid']: {
                    # "name": game['name'],
                    "playtime_disconnected": game['playtime_disconnected'],
                    "playtime_forever": game['playtime_forever'],
                    "playtime_linux_forever": game['playtime_linux_forever'],
                    "playtime_mac_forever": game['playtime_mac_forever'],
                    "playtime_windows_forever": game['playtime_windows_forever'],
                    "rtime_last_played": game['rtime_last_played']
                } for game in data
            }
            self.owned_games = appid_keyed_dict
        return self.owned_games

    def get_appid_name_pair(self):
        return self.get_steam_games()

    def get_user_owned_games(self, steamId):
        owned_games = self.get_owned_games(steamId)
        steam_games = self.get_steam_games()

        for owned_game in owned_games:
            if owned_game in steam_games:
                owned_games[owned_game]['name'] = steam_games[owned_game]
                
        return jsonify(owned_games)

    def get_recently_played_games(self, steamId):
        recent_games = SteamRequest.make_steam_request("IPlayerService/GetRecentlyPlayedGames/v0001", {"steamId": escape(steamId)})
        return jsonify(recent_games)

    def get_specific_game_info(self, steamId, gameId: int):
        owned_games = self.get_owned_games(steamId)
        steam_games = self.get_steam_games()

        for owned_game in owned_games:
            if owned_game in steam_games:
                owned_games[owned_game]['name'] = steam_games[owned_game]
    
        return jsonify(owned_games[int(gameId)])