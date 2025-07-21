import time

_cache = {}
CACHE_TTL = 300  # 5 minutos (pode ajustar)

def get_from_cache(symbol: str):
    now = time.time()
    if symbol in _cache:
        timestamp, data = _cache[symbol]
        if now - timestamp < CACHE_TTL:
            return data
        else:
            del _cache[symbol]
    return None

def set_to_cache(symbol: str, data):
    _cache[symbol] = (time.time(), data)
