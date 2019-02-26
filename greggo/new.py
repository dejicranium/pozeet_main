from greggo.config import REDIS_SERVER

r = REDIS_SERVER

if __name__ == "__main__":
    for i in range(0, 1000):
        print(r.llen('u_f:' + str(i)))