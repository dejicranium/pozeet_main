from pyramid.view import view_config
from ..models.main_models import *

from greggo.storage.redis.voters_age_storage import PollVotersAgeStorage
from greggo.storage.redis.voters_gender_storage import PollVotersGenderStorage
from greggo.config import REDIS_SERVER
from greggo.storage.redis.trending_storage import (TrendingPollsStorage, TrendingOpinionsStorage, TrendingCommentsStorage)

from ..utils.scraper_util import get_page_thumb_title_desc, url_exists, get_first_url
from ..utils.compile_util import compile_poll_details, compile_opinion_details
from pyramid.response import Response
import transaction
from pyramid.httpexceptions import HTTPFound
import uuid
from sqlalchemy import or_, and_
from ..services.activity_service import get_source
from ..services.follow_service import FollowService
from ..services.auth_service import upload_profile_picture



def get_poll_voters_id(poll):
    voter_ids = []
    voters_queryset = poll.voters
    for voter in voters_queryset:
        voter_ids.append(voter.id)
    return voter_ids


@view_config(route_name="load_followers", renderer="json")
def load_followers(request):
    pass


@view_config(route_name="add_new_follower_acts", renderer="json")
def add_new_follower_acts(request):
    follower_id = request.params.get('user_id', None)
    followee_id = request.params.get('to_follow_id', None)
    activities = None
    activity_ids_list = []

    if follower_id and follower_id:
        # get activities of user that is being followed
        activities = request.dbsession.query(Activity).filter(Activity.user_id == followee_id).order_by(Activity.created.desc()).limit(5)

    for activity in activities:
        # we only need the activity id
        activity_ids_list.append(activity.id)
    return {"activities": activity_ids_list, "id": follower_id}


@view_config(route_name="remove_followers_acts", renderer='json')
def remove_followers_acts(request):
    user_id = request.params.get("user_id", None)
    to_unfollow_id = request.params.get("to_unfollow_id", None)

    activities_list = []

    if user_id and to_unfollow_id:
        activities = request.dbsession.query(Activity).filter(Activity.user_id == to_unfollow_id)

        for activity in activities:
            activities_list.append(activity.id)

        return {'activities': activities_list}


@view_config(route_name="load_followees_activities", renderer='json')
def load_followees_activities(request):
    users = request.dbsession.query(User)
    pass


def resolve_voters_data(request):
    activities = request.dbsession.query(Activity)

    # first clear the whole redis cache
    age_storage = PollVotersAgeStorage

    for activity in activities:
        source = get_source(request, activity)
        if source == Poll:
            source_id =  activity.source_id
            voters_age_storage = PollVotersAgeStorage(source_id, REDIS_SERVER)
    pass


@view_config(route_name="add_to_trending", renderer='json')
def add_to_trending(request):

    share = request.dbsession.query(Like)
    share.delete()
    share = request.dbsession.query(Share)
    share.delete()
    share = request.dbsession.query(Reply)
    share.delete()
    agrees = request.dbsession.query(Comment)
    agrees.delete()
    options = request.dbsession.query(Option)
    options.delete()
    polls = request.dbsession.query(Poll)
    context_images = request.dbsession.query(ContextImage)
    context_images.delete()
    context_images = request.dbsession.query(SeenResults)
    context_images.delete()
    context_images = request.dbsession.query(OpinionVotes)
    opinions = request.dbsession.query(Opinion)
    opinions.delete()
    context_images.delete()
    activities = request.dbsession.query(Notification)
    activities.delete()


    polls.delete()
    """
    for poll in polls:
        try:
            poll.delete()
        except Exception as e:
            return {'status': e} 

    for opinion in opinions:
        try: 
            opinion.delete()
        except Exception as e:
            return {'status': e}
    """
    """
    activities = request.dbsession.query(Activity).all()
    for activity in activities: 
        if activity:
            try:
                source = get_source(request, activity)
                if source == Poll: 
                    poll_id = activity.source_id
                    poll = request.dbsession.query(Poll).filter(Poll.id == poll_id).first()
                    # the redis trending poll storage
                    trending_poll = TrendingPollsStorage()

                    trending_poll.add_poll(poll)
                elif source == Opinion:
                    opinion_id = activity.source_id
                    opinion = request.dbsession.query(Opinion).filter(Opinion.id == opinion_id).first()
                    trending_opinion = TrendingOpinionsStorage()
                    trending_opinion.add_opinion(opinion)

                elif source == Comment:
                    comment_id = activity.source_id
                    comment = request.dbsession.query(Comment).filter(Comment.id == comment_id).first()
                    trending_comment = TrendingCommentsStorage()
                    trending_comment.add_comment(comment)
            except Exception as e: 
                return {'status': e}
    """

def populate_demographics(request):
    activities = request.dbsession.query(Activity).all()
    for activity in activities: 
        if activity:
            try:
                source = get_source(request, activity)
                if source == Poll: 
                    poll_id = activity.source_id
                    poll = request.dbsession.query(Poll).filter(Poll.id == poll_id).first()
                    # the redis trending poll storage
                    trending_poll = TrendingPollsStorage()

                    trending_poll.add_poll(poll)
                elif source == Opinion:
                    opinion_id = activity.source_id
                    opinion = request.dbsession.query(Opinion).filter(Opinion.id == opinion_id).first()
                    trending_opinion = TrendingOpinionsStorage()
                    trending_opinion.add_opinion(opinion)

                elif source == Comment:
                    comment_id = activity.source_id
                    comment = request.dbsession.query(Comment).filter(Comment.id == comment_id).first()
                    trending_comment = TrendingCommentsStorage()
                    trending_comment.add_comment(comment)
            except Exception as e: 
                return {'status': e}