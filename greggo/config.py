import redis

sREDIS_SERVER = redis.StrictRedis(host="pozeet-redis-cluster.0jy3so.ng.0001.use2.cache.amazonaws.com", port="6379", db=0)
#REDIS_SERVER = redis.Redis()
def change_redis_connection():
    pass
