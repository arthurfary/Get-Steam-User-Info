from dotenv import load_dotenv
from functools import wraps
from markupsafe import escape

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

    # decorator that converts url to id when needed
    @staticmethod
    def resolve_steam_id(func):
        @wraps(func)
        def wrapper(id_or_url, *args, **kwargs):
            if id_or_url.isnumeric():
                id = int(id_or_url)
            else:
                id = SteamRequest.parse_vanity_url(id_or_url)
            return func(id, *args, **kwargs)
        return wrapper
    
    def parse_vanity_url(vanityUrl):
        data = SteamRequest.make_steam_request("ISteamUser/ResolveVanityURL/v1", {"vanityurl": escape(vanityUrl)})
        steamid = data['response']['steamid']
        return steamid

