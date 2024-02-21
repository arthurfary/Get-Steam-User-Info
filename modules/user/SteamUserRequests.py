from ..SteamRequest import SteamRequest
from flask import jsonify
from markupsafe import escape

class SteamUserRequests(SteamRequest):
    '''
    This class handles requests for user data.
    '''

    def get_user_summary(self, id):
        user_summary = self.make_steam_request("ISteamUser/GetPlayerSummaries/v0002/", {"steamids": id})
        return jsonify(user_summary)
    
    def get_user_friends(self, id):
        user_friends = self.make_steam_request("ISteamUser/GetFriendList/v0001/", {"relationship": "all", "steamid": id})
        return jsonify(user_friends)