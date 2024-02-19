from ..SteamRequest import SteamRequest
from flask import jsonify
from markupsafe import escape

class SteamGameRequests(SteamRequest):
    '''
    This class contains the functions for requesting game data from steam.
    '''


    def _get_steam_games(self):
        data = SteamRequest.make_steam_request("ISteamApps/GetAppList/v2", {})
        all_games = data['applist']['apps']
        steam_games = {game['appid']: game['name'] for game in all_games}
        return steam_games

    def _get_owned_games(self, steamId):
        data = SteamRequest.make_steam_request("IPlayerService/GetOwnedGames/v0001", {"steamId": escape(steamId)})['response']['games']
        owned_games = {
            game['appid']: {
                "playtime_forever": game['playtime_forever'],
                **{ # ** decompresses the rest if the return if there is one
                    key: game[key] for key in ("playtime_disconnected", "playtime_linux_forever", "playtime_mac_forever", "playtime_windows_forever", "rtime_last_played")
                    if key in game
                }
            }
            for game in data
        }
        return owned_games

    def _append_names(self, owned_games, steam_games):
        for appid, game_data in owned_games.items():
            game_name = steam_games.get(appid)
            if game_name:
                game_data['name'] = game_name
        return owned_games
    
    def _get_games(self, steamId):
        owned_games = self._get_owned_games(steamId)
        steam_games = self._get_steam_games()
        self._append_names(owned_games, steam_games) 
        return owned_games

    ###

    def get_appid_name_pair(self):
        steam_games = self._get_steam_games()
        return steam_games

    def get_user_owned_games(self, steamId):
        owned_games = self._get_games(steamId)
        return jsonify(owned_games)

    def get_recently_played_games(self, steamId):
        recent_games = SteamRequest.make_steam_request("IPlayerService/GetRecentlyPlayedGames/v0001", {"steamId": escape(steamId)})
        return jsonify(recent_games)

    def get_specific_game_info(self, steamId, gameId: int):
        owned_games = self._get_games(steamId)
        specific_game = owned_games.get(int(gameId))  # need to make a more explicit error handler

        if specific_game:
            return jsonify(specific_game)
        else:
            # Handle game not found error
            return "Key not found"