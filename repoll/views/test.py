from dateutil import relativedelta
import datetime
import time

def try_something():
    then = datetime.datetime.utcnow()
    time.sleep(10)
    now = datetime.datetime.utcnow()

    difference = relativedelta.relativedelta(now, then)
    print ("minutes difference is " + str(difference.seconds))



if __name__ == "__main__":
    try_something()