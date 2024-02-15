import requests

class SteamGames:
    def __init__(self):
        self.games = self.fetch_games_from_steam()

    def get_games(self):
        return self.games
    
    def fetch_games_from_steam(self):
        data = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2", {}).json()
        all_games = data['applist']['apps']
        self.games = {game['appid']: game['name'] for game in all_games}
        return self.games
