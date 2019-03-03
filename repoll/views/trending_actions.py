from ..utils.compile_util import (
    compile_poll_details,
    compile_opinion_details,
    compile_comment_details,
    normalize_redis_data)

from pyramid.view import view_config

from greggo.storage.redis.timeline_storage import (
    TrendingPollsStorage,
    TrendingCommentsStorage,
    TrendingOpinionsStorage)

from ..models.main_models import (
    Comment,
    User,
    Poll,
    Opinion)


@view_config(route_name='trending_polls', renderer="json")
def get_trending_polls(request):
    trending_polls_list = []
    trending_polls_dictt = {'polls': []}
    user = request.dbsession.query(User).filter(User.id==request.user.id).fist()
    polls_id = TrendingPollsStorage().get_polls()

    # make sure that they are converted to int
    polls_id = normalize_redis_data(polls_id)
    polls_id = [int(_id) for _id in polls_id]
    polls = request.dbsession.query(Poll).filter(Poll.id.in_(polls_id))
    
    for poll in polls:
        trending_polls_list.append(compile_poll_details(request, poll, user))

    trending_polls_dictt['polls'] = trending_polls_list
    return trending_polls_dictt


@view_config(route_name='trending_comments', renderer="json")
def get_trending_comments(request):
    trending_comments_list = []
    trending_comments_dictt = {'comments': []}
    user = request.dbsession.query(User).filter(User.id==request.user.id).first()
    comments_id = TrendingCommentsStorage().get_comments()

    # sanitize
    comments_id = normalize_redis_data(comments_id)
    comments_id = [int(comment_id) for comment_id in comments_id]
    comments = request.dbsession.query(Comment).filter(Comment.id.in_(comments_id))

    for comment in comments:
        trending_comments_list.append(compile_comment_details(request, comment, user))

    trending_comments_dictt['comments'] = trending_comments_list
    return trending_comments_dictt


@view_config(route_name="trending_opinions", renderer='json')
def get_trending_opinions(request):
    trending_opinions_list = []
    trending_opinions_dictt = {'opinions': []}
    user = request.dbsession.query(User).filter(User.id==request.dbsession.id).first()
    opinions_id = TrendingOpinionsStorage().get_opinions()
    opinions_id = normalize_redis_data(opinions_id)
    opinions_id = [int(opinion_id) for opinion_id in opinions_id]

    opinions = request.dbsession.query(Opinion).filter(Opinion.id.in_(opinions_id))

    for opinion in opinions:
        trending_opinions_list.append(compile_opinion_details(request, opinion, user))

    trending_opinions_dictt['opinions'] = trending_opinions_list
    return trending_opinions_dictt

