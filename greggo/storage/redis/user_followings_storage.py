from greggo.storage.redis.structures.set import RedisSet
import requests
import json
from greggo.feed.base import UserFeed

class BaseFollowings(RedisSet):
    def __init__(self, key, redis=None):
        super().__init__(key, redis)


class UserFollowings(BaseFollowings):
    key_format = 'u_fing:%(user_id)s'


    def __init__(self, user_id, redis=None):
        key = self.key_format % {'user_id': user_id}
        super().__init__(key, redis)

    def follow_user(self, followee_id):
        self.add(followee_id)

    def get_followees(self):
        followees =  self.get_all()
        followees = [int(followee.decode('utf-8')) for followee in followees]
        return followees

    def unfollow_user(self, followee_id):
        self.delete(followee_id)

    def is_following_user(self, followee_id):
        return self.exists(followee_id)


class UserFollowers(BaseFollowings):
    key_format = 'u_fll:%(user_id)s'

    def __init__(self, user_id, redis=None):
        key = self.key_format % {'user_id': user_id}
        super().__init__(key, redis)

    def get_followers(self):
        followers = self.get_all()
        followers =  [int(follower.decode('utf-8')) for follower in followers]
        return followers

    def add_new_follower(self, follower_id):
        self.add(follower_id)

    def remove_follower(self, follower_id):
        self.delete(follower_id)



class FollowingsManager:
    @classmethod
    def load_in_followers(cls, user_id, list_of_followers):
        followers_store = UserFollowers(user_id)
        followers_store.add_new_follower(list_of_followers)

    @classmethod
    def load_in_followees(cls, user_id, list_of_followees):
        followees_store = UserFollowings(user_id)
        followees_store.follow_user(list_of_followees)

    @classmethod
    def user_is_following(cls, user1_id, user2_id, redis=None):
        followings =UserFollowings(user1_id, redis)
        return followings.is_following_user(user2_id)

    @classmethod
    def follow_user(cls, user_id, to_follow_id):
        UserFollowings(user_id).follow_user(to_follow_id)
        UserFollowers(to_follow_id).add_new_follower(user_id)
        cls.add_new_follower_latest_activities(user_id, to_follow_id)

    @classmethod
    def add_new_follower_latest_activities(cls, user_id, to_follow_id):
        """
        (TESTED AND WORKS)

        Adds new followers activities to user's feed

        :param user_id: the id of user that is initiating the follow
        :type user_id: int

        :param to_follow_id: the id of the user to be followed
        :type to_follow_id: int

        :return: null
        """

        payload = {'user_id': user_id, 'to_follow_id': to_follow_id}
        response = requests.get('http://localhost:6543/add_new_follower_acts', params=payload)
        json_response = json.loads(response.text)
        activities = json_response['activities']

        # then add activities to user's feed

        user_feed = UserFeed(user_id)
        for activity in activities:
            user_feed.add_activities(activity)




    @classmethod
    def delete_all_followers_activities(cls, user_id, to_unfollow_id):
        """
        (TESTED AND WORKED)

        This removes every activity of someone who a user want's to unfollow from his or her feed.

        :param user_id: user that wants to unfollow another user
        :type user_id: int

        :param to_unfollow_id: user that is to be unfollowed
        :type user_id: int

        :return: null
        """
        payload = {'user_id': user_id, 'to_unfollow_id': to_unfollow_id}
        response = requests.get('http://localhost:6543/remove_followers_acts', params=payload)
        json_data = json.loads(response.text)
        to_unfollow_activities = json_data['activities']

        user_feed = UserFeed(user_id)

        # remove each activity
        for activity in to_unfollow_activities:
            user_feed.remove_activities(activity)


    @classmethod
    def unfollow_user(cls, request, user_id, to_unfollow_id):
        UserFollowings(user_id).unfollow_user(to_unfollow_id)
        UserFollowers(to_unfollow_id).remove_follower(user_id)
        cls.delete_all_followers_activities(user_id, to_unfollow_id)


if __name__ == "__main__":
    print(FollowingsManager.delete_all_followers_activities(1, 1))
