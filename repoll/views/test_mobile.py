from ..models.main_models import *
from pyramid.view import view_config
from ..services.feed_service import (
									return_polls_voted_in, 
									get_activities_if_authenticated,
									get_activities_if_not_autheticated
									)
import random

from greggo.storage.redis.trending_storage import *
from repoll.utils.compile_util import *
@view_config(route_name='mobile_feed', renderer='../templates/new.jinja2', user_agent="mobile")
def home_feed(request):
	if request.user:
		user = request.dbsession.query(User).filter(User.id==request.user.id).first()
		return {'er': '', 'user': user}
	return {'user': False}


@view_config(route_name='get_latest_posts', renderer='json')
def get_activities(request):
	page = request.params.get("page")
	already_shown = []
	if request.user:
		user = request.dbsession.query(User).filter(User.id==request.user.id).first()
		request.response.headers.update({
			'Access-Control-Allow-Origin': '*',
		})
		activities = get_activities_if_authenticated(request, user, page)
		return activities
	else: 
		return get_activities_if_not_autheticated(request, page)


@view_config(route_name='trending_page', renderer='../templates/trending_mobile_page.jinja2')
def trending_page(request):
	if request.user:
		user = request.dbsession.query(User).filter(User.id==request.user.id).first()
	else:
		user = False
	return {'er': 'er', 'user': user}


@view_config(route_name="insert", renderer="json")
def insert(request):
	dictt = {'result': ""}
	poll = request.matchdict.get("poll_id", None)
	snake = request.matchdict.get("snake_id", None)
	if poll:
		dictt['result'] = poll
	elif snake:
		dictt['result'] = snake
	else:
		dictt['result'] = "no poll"
	return dictt


@view_config(route_name="number_of_activities", renderer="json")
def number_of_activities(request):
	activities = request.dbsession.query(Activity)
	length = activities.count()
	return {'len': length}


@view_config(route_name="index", renderer="../templates/index.jinja2", user_agent="mobile")
def index(request):
	return {}

