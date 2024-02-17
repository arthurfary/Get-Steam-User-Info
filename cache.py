from flask_caching import Cache

config = {   
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 10 #s
}

cache = Cache(config=config)