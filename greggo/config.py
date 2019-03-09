import redis

REDIS_SERVER = redis.StrictRedis(host="pozet-redis.0jy3so.ng.0001.use2.cache.amazonaws.com", port="6379", db=0)

# REDIS_SERVER = redis.Redis()


def change_redis_connection():
    pass
