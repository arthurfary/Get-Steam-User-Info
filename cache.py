from flask_caching import Cache

config = {   
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300 #s
}

cache = Cache(config=config)