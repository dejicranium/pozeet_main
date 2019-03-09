from greggo.storage.redis.structures.set import RedisSet
from greggo.config import  REDIS_SERVER
import random

class ActiveCategoriesSubscribers(RedisSet):
    key_format = 'a_u_c:%(category_id)s'

    def __init__(self, key, redis=None):
        if not redis:
            self.redis = REDIS_SERVER
        key = self.key_format % {'category_id': key}
        super().__init__(key, self.redis)

    def add_user(self, user_id):
        # we wish to store only 500 latest active users
        # so if there are 500 users in a particular storage
        # pop one person off, then add your new user
        if self.count() == 200:
            self._pop(1)
            self.add(user_id)
        return 0

    def get_random_users(self, count):
        users_list = self.get_all()
        users_list = list(users_list)
        return random.sample(users_list, count)
