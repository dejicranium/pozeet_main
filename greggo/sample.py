import redis
from greggo.config import REDIS_SERVER

r = REDIS_SERVER
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
    for i in range(0, 100):
        r.spop('u_fd:' + str(i))