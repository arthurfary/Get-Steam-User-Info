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
    def make_steam_request(endpoint, params = {}):
        base_url = f"https://api.steampowered.com/{endpoint}"
        params["key"] = SteamRequest.STEAM_API_KEY
        params["format"] = "json"
        response = requests.get(base_url, params=params)
        return response.json()

    def resolve_id(id):
        id = int(id)
        # check if id is valid
        req = SteamRequest.make_steam_request("ISteamUser/GetPlayerSummaries/v0002/", {'steamids':id})

        if len(req['response']['players']) > 0:
            return id
        else:
            raise BadRequest("Invalid User Id")

    def resolve_url(url):
        data: dict = SteamRequest.make_steam_request("ISteamUser/ResolveVanityURL/v1", {"vanityurl": escape(url)})
        if data.get('response', {}).get('message'): #no match 
            raise BadRequest("Invalid User Url")
        else:
            steamid = data['response']['steamid']
            return steamid
    
    @staticmethod
    def resolve_steam_id(id_or_url):
        if id_or_url.isnumeric(): # if its numeric its a id
            return SteamRequest.resolve_id(id_or_url)
        else:
            return SteamRequest.resolve_url(id_or_url)
    
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
                
            except BadRequest as e:
                error_message = e.description
                return jsonify({"response": {"status": 400, "message": error_message}})
            
            # comment this for debbuging
            except Exception:
                return jsonify({"response": {"status": 500, "message": "An error occurred"}})

        return decorated_function