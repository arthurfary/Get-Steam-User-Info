from dotenv import load_dotenv
import os
import requests

load_dotenv()

class SteamRequest:
    STEAM_API_KEY = os.getenv("STEAM_API_KEY")

    @staticmethod
    def make_steam_request(endpoint, params):
        base_url = f"https://api.steampowered.com/{endpoint}"
        params["key"] = SteamRequest.STEAM_API_KEY
        params["format"] = "json"
        response = requests.get(base_url, params=params)
        return response.json()
