import requests

class SteamGames:
    games = None

    @staticmethod
    def get_games():
        if SteamGames.games is None:
            SteamGames.fetch_games_from_steam()
        return SteamGames.games
    
    @staticmethod
    def fetch_games_from_steam():
        data = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2", {}).json()
        all_games = data['applist']['apps']
        SteamGames.games = {game['appid']: game['name'] for game in all_games}
        return SteamGames.games
