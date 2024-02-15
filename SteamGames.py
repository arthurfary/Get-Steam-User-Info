import requests

class SteamGames:
    def __init__(self):
        self.games = {game['appid']: game['name'] for game in self.fetch_games_from_steam()}

    def get_games(self):
        return self.games
    
    def fetch_games_from_steam(self):
        data = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2", {}).json()
        self.games = data['applist']['apps']
        return self.games
