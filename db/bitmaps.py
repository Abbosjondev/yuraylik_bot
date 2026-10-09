from cachetools import TTLCache
from pyroaring import BitMap64

user_records = BitMap64()
offer_accepted_users = BitMap64()
rating_cache = TTLCache(maxsize=1, ttl=3600)