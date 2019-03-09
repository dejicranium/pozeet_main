from pyramid.view import view_config
from ..models.main_models import (
    User,
    Option,
    OpinionVotes,
    Opinion,
    ContextImage)

from greggo.storage.redis.voters_age_storage import OpinionVotersAgeStorage
from greggo.storage.redis.voters_gender_storage import OpinionVotersGenderStorage
from greggo.storage.redis.trending_storage import TrendingOpinionsStorage
from greggo.storage.redis.active_categories_subscribers_storage import  ActiveCategoriesSubscribers

from ..services.metrics_service import MetricsAggregator
from ..utils.compile_util import return_polls_voted_in, return_opinions_voted_in
from ..utils.compile_util import compile_opinion_details
from ..services.activity_service import ActivityService
import transaction
import uuid
from ..services.auth_service import add_image_description
from ..utils.compile_util import return_categories_subscribed_to
from ..utils.scraper_util import url_exists, get_first_url, get_page_thumb_title_desc
from ..services.follow_service import FollowService


@view_config(route_name='create_opinion', renderer='json')
def create_opinion(request):
    options = []
    opinion = request.params.get('opinion') 
    opinion_image = request.params.get('opinion-image', None)
    user = request.dbsession.query(User).filter(User.id==request.user.id).first()
    new_opinion = Opinion()
    new_opinion.opinion = opinion
    new_opinion.user_id = request.user.id

    # check if there's a url in the opinion
    if url_exists(new_opinion.opinion):
        try:
            url_in_opinion = get_first_url(new_opinion.opinion)
            context_thumb, context_title, context_description = get_page_thumb_title_desc(url_in_opinion)
        # store
            new_opinion.context_page_thumb = context_thumb
            new_opinion.context_page_title = context_title
            new_opinion.context_page_description = context_description
        except:
            print('do nothing')
    request.dbsession.add(new_opinion)
    request.dbsession.flush()

    if opinion_image != None:
        if hasattr(opinion_image, 'file'):
            image_file = opinion_image.file
            image_name = "{}".format(uuid.uuid4())
            uploaded_image = add_image_description(image_file, image_name)
            image_link = uploaded_image['secure_url']
            
            context_image = ContextImage()
            context_image.image_link = image_link
            context_image.opinion_id = new_opinion.id
            request.dbsession.add(context_image)
            transaction.commit()

    new_option1= Option()
    new_option1.title = "Agree"
    options.append(new_option1)

    new_option2 = Option()
    new_option2.title = "Disagree"
    options.append(new_option2)

    new_opinion.options = options
    request.dbsession.add(new_opinion)
    request.dbsession.flush()

    # add opinion to trends
    trend = TrendingOpinionsStorage()
    trend.add_opinion(new_opinion)

    # get the categories that user has subscribed to
    subscriptions = return_categories_subscribed_to(request, user)

    new_activity = ActivityService(request, 'opinion', request.user, new_opinion)
    new_activity.create_new_activity(subscriptions)
    transaction.commit()

    # since user has successfully created opinion activity, just add him to the list of active subscribers in
    # each category that he is subscribed to.
    # first, get activities subscribed to
    subscriptions = return_categories_subscribed_to(request, user)
    for subscription in subscriptions:
        active_subscribers_storage = ActiveCategoriesSubscribers(key=subscription)
        active_subscribers_storage.add_user(request.user.id)

    # return the freshly created opinion
    newly_created_opinion = compile_opinion_details(request, new_opinion, user)
    return newly_created_opinion 


# @view_config(route_name='agree_with_opinion', renderer)
@view_config(route_name='opinion_metrics', renderer='../templates/show_opinion_metrics.jinja2',)
def get_opinion_metrics(request):
    opinion_id = request.matchdict.get('opinion_id', -1)
    # we need to get details the opinion like name and stuff
    opinion = request.dbsession.query(Opinion).filter(Opinion.id==opinion_id).first()
    return {'opinion': opinion}


@view_config(route_name='get_opinion_metrics', renderer='json')
def get_metrics(request):
    main_focus = request.params.get('m_f')
    sub_focus = request.params.get('s_f')
    main_focus_objects = request.params.get('m_f_objs')
    sub_focus_objects = request.params.get('s_f_objs')
    opinion_id = request.matchdict.get('opinion_id')

    # we can't pass a list through the params, so let's get the sub
    # the sub_focus_object when it is options
    if sub_focus_objects == 'options':
        opinion = request.dbsession.query(Opinion).filter(Opinion.id==opinion_id).first()
        sub_focus_objects = [option.id for option in opinion.options]
    else:
        if main_focus == 'age_range':
            sub_focus_objects = sub_focus_objects
        else:
            sub_focus_objects = int(sub_focus_objects)
    
    if main_focus and sub_focus and main_focus_objects and sub_focus_objects and opinion_id:
        request.response.status = '200'
    else:
        request.response.status = '400'

    new_metrics = MetricsAggregator(main_focus, main_focus_objects, sub_focus, sub_focus_objects, opinion_id)
    
    store = None
    if main_focus == 'age' or main_focus == 'age_range':
        store = OpinionVotersAgeStorage
    elif main_focus == 'gender':
        store = OpinionVotersGenderStorage

    derived_metrics = new_metrics.get_metrics(store)
    return derived_metrics


@view_config(route_name='view_opinion_page', renderer='../templates/view_opinion_mobile.jinja2')
def view_opinion_page(request):
    opinion_id = request.matchdict.get('opinion_id')
    opinion = request.dbsession.query(Opinion).filter(Opinion.id==opinion_id).first()
    return {"opinion": opinion, "title": "View opinion by {}".format(opinion.added_by.full_name) }


@view_config(route_name='view_opinion', renderer='json')
def view_opinion(request):
    opinion_id = request.matchdict.get('opinion_id', None)
    opinion = request.dbsession.query(Opinion).filter(Opinion.id==int(opinion_id)).first()

    if request.user:
        user  = request.dbsession.query(User).filter(User.id==request.user.id).first()

    dictt = {
        # check if the user is logged in
        'userLoggedIn': True if request.user is not None else False,
        'id': opinion.id,
        'type': 'opinion',
        'userId': opinion.added_by.id,
        'userName': opinion.added_by.full_name,
        'userPic': opinion.added_by.profile_picture,
        'opinion': opinion.opinion,
        'numOfVotes': opinion.num_of_votes,
        'numOfComments': opinion.num_of_comments,
        'numOfShares': opinion.num_of_shares,
        'numOfLikes': opinion.num_of_likes,
        'timeAdded': opinion.time_added,
        'contextImage': [
            {'imgLink': img.image_link} for img in opinion.context_images
            ]
    }
    if request.user:
        dictt['userHasVoted'] = int(opinion_id) in return_opinions_voted_in(request, user) or opinion.user_id == request.user.id
    else:
        dictt['userHasVoted'] = False
    dictt['options'] = [{           
                        'id': option.id,
                        'option': option.title,
                        'score': 0 if not option.num_of_votes else option.num_of_votes,

                    } for option in opinion.options]

    return dictt


@view_config(route_name='opinions_voted_in_page', renderer='../templates/opinions_voted_in_page.jinja2', user_agent="mobile")
def opinions_voted_in_page(request):
    user = request.dbsession.query(User).filter(User.id==request.user.id).first()

    return {'user': user}


@view_config(route_name='get_opinions_voted_in', renderer='json')
def get_opinions_voted_in(request):
    user = request.dbsession.query(User).filter(User.id==request.user.id).first()
    dictt = {'activities': []}
    opinions_voted_in = user.opinions_voted_in
    opinions_voted_in = [opinion.id for opinion in opinions_voted_in]

    opinions = request.dbsession.query(Opinion).filter(Opinion.id.in_(opinions_voted_in)).all()

    for opinion in opinions:

        opinion_dictt = compile_opinion_details(request, opinion, user)
        opinion_dictt['userHasVoted'] = True
        dictt['activities'].append(opinion_dictt)

    return dictt


@view_config(route_name="get_voters_on_opinion", renderer="json")
def get_voters_on_opinion(request):
    opinion_id = request.matchdict.get("opinion_id", None)
    voters = []

    if opinion_id:
        opinion = request.dbsession.query(Opinion).filter(Opinion.id == opinion_id).first()
        user = request.dbsession.query(User).filter(User.id == request.user.id).first()
        user_followees = FollowService.get_followees_ids(request, user)
        user_votes = request.dbsession.query(OpinionVotes).filter(OpinionVotes.opinion_id==opinion_id)
        
    for vote in user_votes: 
        user_dict = {}
        user_dict['userId'] = vote.added_by.id
        user_dict['userName'] = vote.added_by.full_name
        user_dict['username'] = vote.added_by.username
        user_dict['userPic'] = vote.added_by.profile_picture
        user_dict['userIsFollowing'] = vote.added_by.id in user_followees
        voters.append(user_dict)
    return voters
