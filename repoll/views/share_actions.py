
from pyramid.view import view_config
from ..models.main_models import *
from pyramid.response import Response
from ..services.activity_service import ActivityService
import transaction
from pyramid.httpexceptions import HTTPFound
from ..services.notification_service import NotificationService


def increase_num_of_shares(source_obj, source_class):
    source_obj.update({"num_of_shares": (source_class.num_of_shares + 1)})

@view_config(route_name='share', renderer='json')
def share(request):
    body = request.json_body
    poll_id = body.get('poll_id', None)
    reply_id = body.get('reply_id', None)
    comment_id = body.get('comment_id', None)
    opinion_id = body.get('opinion_id', None)
    
    new_share = Share()
    new_share.user_id = request.user.id

    if poll_id:
        poll_obj = request.dbsession.query(Poll).filter(Poll.id==poll_id)
        poll = poll_obj.first()

        new_share.poll_id = poll_id
        request.dbsession.add(new_share)
        request.dbsession.flush()

        increase_num_of_shares(poll_obj, Poll)

        new_activity = ActivityService(request, 'share', request.user, new_share, poll)
        new_activity.create_new_activity()
        transaction.commit()

        created_activity = new_activity.get_activity()
        user_id = created_activity.object_owner_id
        sender_id = request.user.id
        activity_type = created_activity.activity_type
        source = new_share
        _object = poll

        new_notification = NotificationService(request, user_id, sender_id, activity_type, _object)
        new_notification.create_new_notification()
        transaction.commit()

    
    if opinion_id:
        opinion_obj = request.dbsession.query(Opinion).filter(Opinion.id==opinion_id)
        opinion = opinion_obj.first()

        new_share.opinion_id = opinion_id
        request.dbsession.add(new_share)
        request.dbsession.flush()

        increase_num_of_shares(opinion_obj, Opinion)

        new_activity = ActivityService(request, 'share', request.user, new_share, opinion)
        new_activity.create_new_activity()
        transaction.commit()
        

        created_activity = new_activity.get_activity()

        user_id = created_activity.object_owner_id
        sender_id = request.user.id
        activity_type = created_activity.activity_type
        source = new_share
        _object = opinion

        new_notification = NotificationService(request, user_id, sender_id, activity_type, source, _object)
        new_notification.create_new_notification()
    
    if comment_id:
        comment_obj = request.dbsession.query(Comment).filter(Comment.id == comment_id)
        comment = comment_obj.first()

        new_share.comment_id = comment_id
        request.dbsession.add(new_share)
        request.dbsession.flush()

        increase_num_of_shares(comment_obj, Comment)

        new_activity = ActivityService(request, 'share', request.user, new_share, comment)
        new_activity.create_new_activity()
        transaction.commit()

        created_activity = new_activity.get_activity()
        
        user_id = created_activity.object_owner_id
        sender_id = request.user.id
        activity_type = created_activity.activity_type
        source = new_share
        _object = comment

        new_notification = NotificationService(request, user_id, sender_id, activity_type, source, _object)
        new_notification.create_new_notification()

    if reply_id:
        reply_obj = request.dbsession.query(Reply).filter(Reply.id==reply_id)
        reply = reply_obj.first()

        new_share.reply_id = reply_id
        request.dbsession.add(new_share)
        request.dbsession.flush()

        increase_num_of_shares(reply_obj, Reply)

        new_activity = ActivityService(request, 'share', request.user, new_share, reply)
        new_activity.create_new_activity()
        transaction.commit()

        created_activity = new_activity.get_activity()
        
        user_id = created_activity.object_owner_id
        sender_id = request.user.id
        activity_type = created_activity.activity_type
        source = new_share
        _object = reply

        new_notification = NotificationService(request, user_id, sender_id, activity_type, source, _object)
        new_notification.create_new_notification()


@view_config(route_name="delete_share", renderer="json")
def delete_share(request):
    #delete the share entity
    share_id = request.json_body.get("share_id", None)
    if share_id: 
        share = request.dbsession.query(Share).filer(Share.id==share_id).first()
        request.dbsession.delete(share)
        
        #delete the share activity
        share_activity = request.dbsession.query(Activity).filter(Activity.activity_type =="share", Activity.source_id==share_id).first()
        request.dbsession.delete(share_activity)
        transaction.commit()