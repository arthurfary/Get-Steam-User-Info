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

    @staticmethod
    def resolve_steam_id(id_or_url):
        if id_or_url.isnumeric(): # if its numeric its a id
            return SteamRequest._resolve_id(id_or_url)
        else:
            return SteamRequest._resolve_url(id_or_url)

    def _resolve_id(id):
        id = int(id)
        # check if id is valid
        req = SteamRequest.make_steam_request("ISteamUser/GetPlayerSummaries/v0002/", {'steamids':id})

        if len(req['response']['players']) > 0:
            return id
        else:
            raise BadRequest("Invalid User Id")

    def _resolve_url(url):
        data: dict = SteamRequest.make_steam_request("ISteamUser/ResolveVanityURL/v1", {"vanityurl": escape(url)})
        if data.get('response', {}).get('message'): #no match 
            raise BadRequest("Invalid User Url")
        else:
            steamid = data['response']['steamid']
            return steamid
        