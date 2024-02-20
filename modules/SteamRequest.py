from dotenv import load_dotenv
from functools import wraps
from markupsafe import escape

from flask import jsonify
from werkzeug.exceptions import BadRequest

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
    def resolve_steam_id(id_or_url):
        if id_or_url.isnumeric():
            id = int(id_or_url)
        else:
            id = SteamRequest.parse_vanity_url(id_or_url)
        return id

    def parse_vanity_url(vanityUrl):
        data: dict = SteamRequest.make_steam_request("ISteamUser/ResolveVanityURL/v1", {"vanityurl": escape(vanityUrl)})
        if data.get('response', {}).get('message'): #no match 
            return None
        else:
            steamid = data['response']['steamid']
            return steamid
    
    def resolve_steam_id_and_handle_error(f):
        '''
        Decorator that converts vanity URL to Steam ID, checks validity,
        and ensures consistent JSONified error responses.
        '''

        @wraps(f)
        def decorated_function(id_or_url, *args, **kwargs):
            try:
                steam_id = SteamRequest.resolve_steam_id(id_or_url)
                if steam_id:
                    return f(steam_id, *args, **kwargs)
                else:
                    raise BadRequest("Invalid User ID or URL")
            except Exception as e:
                # Catch any potential errors during resolution
                error_message = str(e)
                return jsonify({"response": {"status": 500, "message": error_message}})

        return decorated_function