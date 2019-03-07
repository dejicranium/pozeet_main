from pyramid.view import view_config
from ..models.main_models import *
import transaction
from greggo.storage.redis.voters_age_storage import PollVotersAgeStorage, OpinionVotersAgeStorage
from greggo.config import REDIS_SERVER
from greggo.storage.redis.voters_gender_storage import PollVotersGenderStorage, OpinionVotersGenderStorage
from ..services.activity_service import ActivityService
from ..utils.compile_util import (
                                return_polls_voted_in, 
                                return_opinions_voted_in, 
                                return_comments_shared,
                                compile_poll_details,
                                compile_opinion_details,
                                compile_reply_details,
                                )
from ..utils.compile_util import compile_comment_details as compile_comment_for_feed
from greggo.storage.redis.trending_storage import TrendingCommentsStorage, TrendingPollsStorage
from repoll.services.notification_service import *
from repoll.services.activity_service import ActivityService


def compile_comments(request, comment):
    comment_dictt = {'replies': []}
    is_poll_comment = False
    is_opinion_comment = False
    user = None
    try:
        is_poll_comment = comment.poll_id is not None
    except:
        print("s")
    try:
        is_opinion_comment = comment.opinion_id is not None
    except:
        print("s")
    if request.user:
        user = request.dbsession.query(User).filter(User.id == request.user.id).first()
    comment_dictt['id'] = comment.id
    comment_dictt['userName'] = comment.added_by.full_name
    comment_dictt['username'] = comment.added_by.username

    comment_dictt['type'] = 'comment'
    comment_dictt['option'] = comment.option.title
    comment_dictt['optionId'] = comment.option.id
    comment_dictt['comment'] = comment.comment
    comment_dictt['userPic'] = comment.added_by.profile_picture
    comment_dictt['numOfAgrees'] = comment.num_of_agrees
    comment_dictt['numOfShares'] = comment.num_of_shares
    comment_dictt['numOfLikes'] = comment.num_of_likes
    comment_dictt['optionChosen'] = comment.option.title

    for reply in comment.replies:
        reply_dictt = compile_reply_details(request, reply, user)
        comment_dictt['replies'].append(reply_dictt)
    
    if request.user:
        comment_dictt['hasSharedComment'] = comment.id in return_comments_shared(request, user)
        comment_dictt['userHasLiked'] = request.user.id in [like.user_id for like in comment.likes]
    else:
        comment_dictt['hasSharedComment'] = False

    if is_poll_comment:
        comment_dictt['poll'] = compile_poll_details(request, comment.poll, user)
    elif is_opinion_comment:
        comment_dictt['opinion'] = compile_opinion_details(request, comment.opinion, user)

    
    return comment_dictt



@view_config(route_name='view_comments', renderer='json')
def view_comments(request):
    poll_id = request.matchdict.get('poll_id', None)
    option_id = request.params.get('option_id', None)
    dictt = {'comments':[]}
    if option_id:
        comments = request.dbsession.query(Comment).filter(Comment.poll_id==poll_id)[start:end]
        for comment in comments:
            comment_dictt = compile_comments(request, comment)
            dictt['comments'].append(comment_dictt)
        return dictt
    elif poll_id: 
        comments = request.dbsession.query(Comment).filter(Comment.poll_id==poll_id)
        for comment in comments: 
            comment_dictt = compile_comments(request, comment)
            dictt['comments'].append(comment_dictt)
        return dictt
    else:
        return {'nothing': 'nothing'}


@view_config(route_name='add_comment', renderer='json')
def add_comment(request):
    comment = request.params.get('comment', '')
    option_id = request.params.get('option_id')
    poll_id = request.params.get('poll_id', None)
    opinion_id = request.params.get('opinion_id', None)
    import logging
    
    user = request.dbsession.query(User).filter(User.id==request.user.id).first()
    option = request.dbsession.query(Option).filter(Option.id == option_id)
    try:
        if comment:
            try:
                logging.info("Creating comment class")
                new_comment = Comment()
                new_comment.commenter_id = request.user.id
                new_comment.comment = comment
                new_comment.option_id = option_id
                if poll_id:
                    new_comment.poll_id = poll_id
                elif opinion_id:
                    new_comment.opinion_id = opinion_id
                #create conversation
                conversation = Conversation()
                request.dbsession.add(conversation)
                request.dbsession.flush()
                new_comment.conversation_id = conversation.id
                request.dbsession.add(new_comment)
                request.dbsession.flush()

                #add to the list of trending topics to see if it fits
                t = TrendingCommentsStorage()
                t.add_comment(new_comment)
                
            except Exception as e:
                return {'problem': e}

            if poll_id:
                poll = request.dbsession.query(Poll).filter(Poll.id == poll_id)
                comment = request.dbsession.query(Comment).filter(Comment.id == new_comment.id)
                #add vote
                new_user_vote = PollVotes()
                new_user_vote.user_id = user.id
                new_user_vote.poll_id = poll_id
                #see whether it fits in a set of trends
                t = TrendingCommentsStorage()
                t.add_comment(comment.first())

                #store the vote
                request.dbsession.add(new_user_vote)
                request.dbsession.flush()
                #add as a new activity
                new_activity = Activity()
                new_activity.user_id = request.user.id
                new_activity.activity_type = 'comment'
                new_activity.source_id = new_comment.id
                new_activity.object_id = poll_id
                new_activity.object_owner_id = new_comment.added_by.id
                new_activity.object_name = 'poll'
                activity_service =  ActivityService(request, 'comment', request.user, new_comment, poll.first())
                activity_service.create_new_activity()
                #create a notification
                new_activity = activity_service.get_activity() #get back the just created activity as an object                
                user_id = new_activity.object_owner_id
                sender_id = request.user.id
                activity_type = new_activity.activity_type
                source = new_comment
                _object = poll.first()
                notification = NotificationService(request, user_id, sender_id, activity_type, source, _object)
                notification.create_new_notification()
                #increment necessary details
                poll.update({"num_of_votes" : (Poll.num_of_votes + 1)})
                option.update({"num_of_votes" : (Option.num_of_votes + 1)})

                #save user's age in redis voters age storage
                user_age = user.age
                redis_store = PollVotersAgeStorage(poll_id, REDIS_SERVER)
                redis_store.increment_age(str(user_age) + '::' + str(option_id))

                if user.sex:
                    redis_store = PollVotersGenderStorage(poll_id, REDIS_SERVER)
                    #increment gender_votes
                    if user.sex == 'Male':
                        redis_store.increment_gender_votes(str('M') + '::' + str(option_id))
                    else:
                        redis_store.increment_gender_votes(str('F') + '::' + str(option_id))
               
                #add the poll to the trends again
                p = TrendingPollsStorage()
                p.add_poll(poll.first())

                transaction.commit()
                newly_created_comment = compile_comment_for_feed(request, new_comment, user)
                return newly_created_comment
            else:  #it is an opiion
                opinion = request.dbsession.query(Opinion).filter(Opinion.id == opinion_id)

                new_user_vote = OpinionVotes()
                new_user_vote.user_id = user.id
                new_user_vote.opinion_id = opinion_id

                #store the vote
                request.dbsession.add(new_user_vote)
                request.dbsession.flush()

                activity_service =  ActivityService(request, 'comment', request.user, new_comment, opinion.first())
                activity_service.create_new_activity()

                new_activity = activity_service.get_activity()
                
                user_id = new_activity.object_owner_id
                sender_id = request.user.id
                activity_type = 'comment'
                source = new_comment
                _object = opinion.first()


                notification = NotificationService(request, user_id, sender_id, activity_type, source, _object)
                notification.create_new_notification()
   
                #increment necessary details
                opinion.update({"num_of_votes" : (Opinion.num_of_votes + 1)})
                opinion.update({"num_of_comments" : (Opinion.num_of_comments + 1)})
                
                option.update({"num_of_votes" : (Option.num_of_votes + 1)})            

                option = option.first()
                if option.title == "Agree":
                    opinion.update({"num_of_agrees" : (Opinion.num_of_agrees + 1)})
                elif option.title== "Disagree":
                    opinion.update({"num_of_disagrees": (Opinion.num_of_disagrees + 1)})
                #save user's age in redis voters age storage
                user_age = user.age
                redis_store = OpinionVotersAgeStorage(opinion_id, REDIS_SERVER)
                redis_store.increment_age(str(user_age) + '::' + str(option_id))

                if user.sex:
                    redis_store = OpinionVotersGenderStorage(opinion_id, REDIS_SERVER)
                    #increment gender_votes
                    if user.sex == 'Male':
                        redis_store.increment_gender_votes(str('M') + '::' + str(option_id))
                    else:
                        redis_store.increment_gender_votes(str('F') + '::' + str(option_id))
            
                transaction.commit()
                newly_created_comment = compile_comment_for_feed(request, new_comment, user)
                return newly_created_comment
        else:
            if opinion_id:
                new_user_vote = OpinionVotes()
                new_user_vote.user_id = user.id
                new_user_vote.opinion_id = opinion_id
                opinion = request.dbsession.query(Opinion).filter(Opinion.id == opinion_id)
                
                request.dbsession.add(new_user_vote)
                opinion.update({"num_of_votes" : (Opinion.num_of_votes + 1)})
                opinion.update({"num_of_comments" : (Opinion.num_of_comments + 1)})
                option.update({"num_of_votes" : (Option.num_of_votes + 1)})

                option = option.first()
                if option.title == "Agree":
                    opinion.update({"num_of_agrees": (Opinion.num_of_agrees + 1)})
                elif option.title == "Disagree":
                    opinion.update({"num_of_disagrees": (Opinion.num_of_disagrees + 1)}) 
                user_age = user.age
                redis_store = OpinionVotersAgeStorage(opinion_id, REDIS_SERVER)
                redis_store.increment_age(str(user_age) + '::' + str(option_id))

                if user.sex:
                    redis_store = OpinionVotersGenderStorage(opinion_id, REDIS_SERVER)
                    #increment gender_votes
                    if user.sex == 'Male':
                        redis_store.increment_gender_votes(str('M') + '::' + str(option_id))
                    else:
                        redis_store.increment_gender_votes(str('F') + '::' + str(option_id))

            
            
                transaction.commit() 


    except Exception as e:
        request.response.status = '400'
        return {'status': e}
    
    else:
        request.response.status = '200'
        return {'status': 'success'}


@view_config(route_name='agree_with_comments', renderer='json')
def agree_with_comment(request):
    """
        I need to protect this function from people who would want to agree many times
    """
    json_body = request.json_body
    comment_id = json_body.get('comment_id', None)
    opinion_id = json_body.get('opinion_id', None)
    option_id = json_body.get('option_id', None)
    poll_id = json_body.get('poll_id', None)
    user_id = request.user.id
    new_agree = None

    """
    activity_service = ActivityService
    activity = activity_service.get_activity()

    user_id = activity.object_owner_id
    sender_id = new_user_vote.user_id
    activity_type = activity.activity_type
    source = new_user_vote
    _object =  poll.first()

    notif = NotificationService(request, user_id, sender_id, activity_type, source, _object)
    notif.create_new_notification()
    transaction.commit()
    """

    user = request.dbsession.query(User).filter(User.id==request.user.id).first()
    option = request.dbsession.query(Option).filter(Option.id == option_id)
    comment = request.dbsession.query(Comment).filter(Comment.id == comment_id)

    # we are aggreeing to an opinion
    if comment_id and user_id and option_id: 
        new_agree = Agrees(comment_id=comment_id, user_id=user_id, option_id=option_id)
        request.dbsession.add(new_agree)    
    try:
        if poll_id:
            # store the vote
            poll = request.dbsession.query(Poll).filter(Poll.id == poll_id)
            new_user_vote = PollVotes()
            new_user_vote.user_id = user.id
            new_user_vote.poll_id = poll_id

            # store the vote
            request.dbsession.add(new_user_vote)

            # increment necessary details
            poll.update({"num_of_votes" : (Poll.num_of_votes + 1)})
            option.update({"num_of_votes" : (Option.num_of_votes + 1)})
            comment.update({'num_of_votes': (Comment.num_of_votes + 1)})
            comment.update({'num_of_agrees': (Comment.num_of_agrees + 1)})

            # see whether there's space for the comment in trends
            t = TrendingCommentsStorage()
            t.add_comment(comment.first())

            # save user's age in redis voters age storage
            user_age = user.age
            redis_store = PollVotersAgeStorage(poll_id, REDIS_SERVER)
            redis_store.increment_age(str(user_age) + '::' + str(option_id))

            if user.sex:
                redis_store = PollVotersGenderStorage(poll_id, REDIS_SERVER)
                # increment gender_votes
                if user.sex == 'Male':
                    redis_store.increment_gender_votes(str('M') + '::' + str(option_id))
                else:
                    redis_store.increment_gender_votes(str('F') + '::' + str(option_id))
            transaction.commit()

        elif opinion_id:
            try:
                opinion = request.dbsession.query(Opinion).filter(Opinion.id == opinion_id)
                new_user_vote = OpinionVotes()
                new_user_vote.user_id = user.id
                new_user_vote.opinion_id = opinion_id

                # store the vote
                request.dbsession.add(new_user_vote)

                # increment necessary details
                opinion.update({"num_of_votes" : (Opinion.num_of_votes + 1)})
                option.update({"num_of_votes" : (Option.num_of_votes + 1)})
                comment.update({'num_of_votes': (Comment.num_of_votes + 1)})
                comment.update({'num_of_agrees': (Comment.num_of_agrees + 1)})

                # see whether there's space for the comment in trends
                t = TrendingCommentsStorage()
                t.add_comment(comment.first())

                # save user's age in redis voters age storage
                user_age = user.age
                redis_store = OpinionVotersAgeStorage(poll_id, REDIS_SERVER)
                redis_store.increment_age(str(user_age) + '::' + str(option_id))

                if user.sex:
                    redis_store = OpinionVotersGenderStorage(poll_id, REDIS_SERVER)
                # increment gender_votes
                    if user.sex == 'Male':
                        redis_store.increment_gender_votes(str('M') + '::' + str(option_id))
                    else:
                        redis_store.increment_gender_votes(str('F') + '::' + str(option_id))

                transaction.commit()
            except Exception as e:
                return {'status': e}
        
    except Exception as e:
        raise e
    else:
        request.response.status = '200' 
        return {'status': 'success'}
    

@view_config(route_name='view_opinion_comments', renderer='json')
def get_opinion_comments(request):
    opinion_id = request.matchdict.get('opinion_id', None)
    dictt = {'comments':[]}

    if opinion_id: 
        comments = request.dbsession.query(Comment).filter(Comment.opinion_id==opinion_id)
        for comment in comments: 
            comment_dictt = compile_comments(request, comment)
            dictt['comments'].append(comment_dictt)

        return dictt
    else:
        return {'nothing': 'nothing'}    


@view_config(route_name='view_comment_page', renderer='../templates/view_comment.jinja2', user_agent="mobile")
def view_comment_page(request):
    comment_id = request.matchdict.get('comment_id', None)

    comment = request.dbsession.query(Comment).filter(Comment.id == comment_id).first()
    return {'comment': comment, 'comment_id': comment_id}


@view_config(route_name='get_comment', renderer='json')
def get_comment(request):
    comment_id = request.matchdict.get('comment_id', None)
    comment = request.dbsession.query(Comment).filter(Comment.id == comment_id).first()
    dictt = compile_comments(request, comment)
    return dictt

