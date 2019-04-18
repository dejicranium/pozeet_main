import redis

REDIS_SERVER = redis.StrictRedis(host="52.170.221.191", port="6379", db=0)

#REDIS_SERVER = redis.Redis()


def change_redis_connection():
    pass
