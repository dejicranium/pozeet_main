from ..services.follow_service import FollowService
from pyramid.view import view_config
from ..models.main_models import  User
from greggo.storage.redis.user_followings_storage import FollowingsManager
from greggo.feed.base import *

@view_config(route_name='follow_user', renderer='json')
def follow_user(request):
	user_id = request.user.id
	followed_id = request.matchdict.get('user_id', None)
	if user_id == int(followed_id):
		request.response.status = '400'
		return {'state': "Nice try. But you can't and shouldn't follow yourself"}

	FollowService.follow_user(request, user_id, followed_id)
	
	#store in redis
	FollowingsManager.follow_user(user_id, followed_id)
	
	
	return {'state': 'success'}

@view_config(route_name='unfollow_user', renderer='json')
def unfollow_user(request):
	user_id = request.user.id
	user_to_unfollow_id = request.matchdict.get('user_id', None)

	if user_id and user_to_unfollow_id: 
		try: 
			FollowService.unfollow_user(request, user_id, user_to_unfollow_id)
			return {'status': 'success'}

			#store in redis
			FollowingsManager.unfollow_user(request, user_id, user_to_unfollow_id)
			to_unfollow_activities = request.dbsession.query(Activity).filter(Activity.user_id==user_to_unfollow_id)
			activities_to_unfollow_id = [activity.id for activity in to_unfollow_activities]

			user_feed = UserFeed(request.user.id)
			user_feed.remove_activities(activities_to_unfollow_id)

			
		except Exception as e:
			request.response.status = '500'
			return {'status': 'failed', 'reason': str(e)}
			

@view_config(route_name='followings', renderer='json')
def followings(request):
	user = request.dbsession.query(User).filter(User.id==request.user.id).first()
	followings_dict_list = []
	followings = user.following

	for each in followings:
		followingz = request.dbsession.query(User).filter(User.id == request.user.id).first()
		for following in followingz:
			user_dict = {}
			user_dict['userId'] = following.id
			user_dict['userName'] = following.full_name
			user_dict['username'] = following.username
			user_dict['userPic'] = following.profile_picture
			user_dict['userIsFollowing'] = True
			followings_dict_list.append(user_dict)
	return followings_dict_list


@view_config(route_name="followers", renderer='json')
def get_followers(request):
	user = request.dbsession.query(User).filter(User.id == request.user.id).first()
	followers_dict_list = []
	followers = user.followers
	user_followees = FollowService.get_followees_ids(request, user)

	for each in followers:
		ffls = request.dbsession.query(User).filter_by(id=each.follower_id).all()
		for follower in ffls:
			user_dict = {}
			user_dict['userId'] = follower.id
			user_dict['userName'] = follower.full_name
			user_dict['username'] = follower.username
			user_dict['userPic'] = follower.profile_picture
			user_dict['userIsFollowing'] = follower.id in user_followees
			followers_dict_list.append(user_dict)

	return followers_dict_list
