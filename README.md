# Get-Steam-User-Info
### API Purpose:

-   Retrieves information about Steam games and user game libraries using the Steam Web API in a non cluttered way.

### Endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/games/<steam_id_or_vanity_url>` | GET | Retrieves a list of games owned by a given Steam user. |
| `/games/recent/<steam_id_or_vanity_url>` | GET | Retrieves a list of recently played games for a Steam user. |
| `/games/gameinfo/<steam_id_or_vanity_url>/<appid>` | GET | Retrieves specific information about a game owned by a Steam user. |
| `/games/getAppidNamePair` | GET | Returns a dictionary mapping Steam app IDs to game names. |
| `/users/<steam_id_or_vanity_url>` | GET | Retrieves a steam data of the user. |
| `/users/friends/<steam_id_or_vanity_url>` | GET | Retrieves the friends list of the user. |
| `/users/achievements/<steam_id_or_vanity_url>/<appid>` | GET | Retrieves specific information about achievements for a given owned game. |
