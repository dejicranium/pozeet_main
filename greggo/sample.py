import redis

r = redis.StrictRedis()

def convert_dictt_to_list(dictt):
    return [k for k in dictt.keys()]
def add_something(something):
    key = "abc"
    count = r.scard(key)
    members = r.smembers(key)
    add = r.sadd
    remove = r.srem
    if count == 5 or count > 5:
        members_ = [k for k in members]
        length = len(members_)
        last_member = members_[length-1]
        remove(key, last_member)
        add(key, something)
    else: 
        add(key, something)
    print(members)
if __name__ == "__main__":
    r.rpush('b', 20)
    r.rpush('b', 12)
    print(r.lrange('b', 0, 100))
    r.lrem('b', 0, 20)
    print(r.lrange('b', 0, 20))