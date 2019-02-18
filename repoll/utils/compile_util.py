from ..models.main_models import Share, Reply, Category
from .scraper_util import get_first_url, url_exists, get_page_thumb_title_desc, get_page_desc, get_page_thumb

def return_polls_voted_in(request, user):
	if not request.user:
		return []
	polls_voted_in = []
	for i in user.polls_voted_in:
		polls_voted_in.append(i.poll_id)

	"""for each in user.polls_voted_in: 
		polls = request.dbsession.query(User).filter_by(id=each.user_id).all()
		for poll in polls: 
			polls_voted_in.append(poll)
	"""
	return polls_voted_in


def return_opinions_voted_in(request, user):
	if not request.user:
		return []
	opinions_voted_in = []
	for i in user.opinions_voted_in:
		opinions_voted_in.append(i.opinion_id)
	return opinions_voted_in

def return_categories_subscribed_to(request, user):
	if not request.user:
		return []
	user_categories = []
	for each in user.subscriptions:
		categories = request.dbsession.query(Category).filter_by(id=each.category_id).all()
		for category in categories:
			user_categories.append(category.id)
	return user_categories
	
def return_polls_results_seen_by_user(request, user):
	if not request.user:
		return []
	seen_results = []
	if user:
		for poll in user.polls_seen_results:
			seen_results.append(int(poll.poll_id))
	return seen_results

def return_comments_shared(request, user):
	if not request.user:
		return []
	comments_shared = []
	shares  = request.dbsession.query(Share).filter(Share.user_id==user.id)
	for share in shares:
		if share.comment_id:
			comments_shared.append(share.comment_id)
	return comments_shared


def compile_reply_details(request, reply, user, recursive_replies=False, upward_recursion=False):
	object_is_comment = False
	object_is_reply = False

	try:
		object_is_comment = reply.comment != None
	except:
		print('')
	try:
		object_is_reply = reply.replyObj != None
	except: 
		print('')
	reply_dictt = {
                'id': reply.id,
                'type': 'reply',
				'conversationId': reply.conversation_id,
                'userName': reply.added_by.full_name,
				'username': reply.added_by.username,
                'userPic': reply.added_by.profile_picture,
				'userId': reply.added_by.id,
				'userSlug': reply.added_by.slug,
                'reply': reply.reply,
                'userRepliedTo': reply.user_replied_to.full_name,
                'numOfShares': reply.num_of_shares,
                'numOfLikes': reply.num_of_likes,
				'numOfReplies': reply.num_of_replies,
				'replies': [],
				'timeAdded': reply.time_added,
	}

	if request.user:
		reply_dictt['userHasLiked'] = request.user.id in [like.user_id for like in reply.likes]
	
	if object_is_comment:
		reply_dictt['comment'] = compile_comment_details(request, reply.comment, user)

	#elif object_is_reply:
		#reply_dictt['reply'] = compile_reply_details(request, reply.replyObj, user)

	if reply.replied_id: 
		reply_dictt['type'] = 'replyReply'

	if recursive_replies: 
		if not reply.replies:
			pass
		else: 
			for reply in reply.replies:
				reply_dictt['replies'].append(compile_reply_details(request, reply, user, recursive_replies=True))
	elif upward_recursion:
		if not reply.parent:
			pass
		else:
			reply_dictt['replies'].append(compile_reply_details(request, reply.parent, user, upward_recursion=True))
	return reply_dictt

def compile_poll_details(request, poll, user):
    options_with_image = [option for option in poll.options if option.image_link is not None]

    dictt = {
        'type': 'poll', 
        'id': poll.id, 
        'userName': poll.added_by.full_name,
		'username': poll.added_by.username, 
		'userId': poll.added_by.id,
        'userPic': poll.added_by.profile_picture, 
        'imageInfo': poll.info_image_link,
        'question': poll.question, 
        'info': poll.info, 
        'totalVotes': poll.num_of_votes,
        'slug': poll.slug, 
		'isPicturePoll': options_with_image != [],  #

        'hasUrlInfo': url_exists(poll.info),
        'infoPageThumb': poll.info_link_thumb,

        'infoPageTitle': poll.info_link_title,
        'infoPageDescription': poll.info_link_desc,           
        'hasEnded': poll.has_ended,
		'timeAdded': poll.time_added,
		'timeRemaining': poll.time_remaining,
		'numOfLikes': poll.num_of_likes,
        'options': [
            {
                'id': option.id, 
                'option': option.title,
				'image': option.image_link, 
                'score': 0 if not option.num_of_votes else option.num_of_votes,
            } for option in poll.options],
    } 
	
    if request.user:
        dictt['userHasLiked'] = request.user.id in [like.user_id for like in poll.likes]
        dictt['userHasVoted'] = poll.id in return_polls_voted_in(request, user) or poll.poser == request.user.id
        dictt['userHasSeenResults']= poll.id in return_polls_results_seen_by_user(request, user)
    else:
        dictt['userHasLiked'] = False
        dictt['userHasVoted'] = False
        dictt['userHasSeenResults'] = False
    return dictt  

def compile_opinion_details(request, opinion, user):
    opinion_dictt = {

	    'id':  opinion.id,
		'type': 'opinion',
		'userName': opinion.added_by.full_name,
		'username': opinion.added_by.username,
		'userPic': opinion.added_by.profile_picture,
		'opinion': opinion.opinion,
		'options': [
			{
				'id': option.id,
				'option': option.title,
				'score':  0 if not option.num_of_votes else option.num_of_votes,

			} for option in opinion.options],

		'totalVotes': opinion.num_of_votes,
		'numOfComments': opinion.num_of_comments,
		'numOfShares': opinion.num_of_shares,
		'numOfLikes': opinion.num_of_likes,
		'timeAdded': opinion.time_added, 
        'contextImage': [
                    {'imgLink': img.image_link} for img in opinion.context_images
                    ], 			
                
	}

    if request.user:
        opinion_dictt['userHasVoted'] =  opinion.id in return_opinions_voted_in(request, user) or opinion.user_id == request.user.id
    else: 
        opinion_dictt['userHasVoted'] = False

        
    return opinion_dictt

def compile_comment_details(request, comment, user):
	object_is_poll = False
	object_is_opinion = False
	comment_dictt = {}
	try:
		object_is_poll = comment.poll is not None
	except:
		print('')
	try: 
		object_is_opinion = comment.opinion is not None
	except:
		print('') 

	comment_dictt = {
            'type': 'comment',
            'comment_id': comment.id,
            'userId': comment.added_by.id,
			'username': comment.added_by.username,
            'commenterInitals': comment.added_by.initials,
            'commenter': comment.added_by.full_name,
            'comment': comment.comment,
            'numOfReplies': comment.num_of_replies,
            'option_chosen': comment.option.title,
			'timeAdded': comment.time_added,         
    }
	
	if object_is_poll:
		poll = comment.poll
		comment_dictt['poll'] = compile_poll_details(request, poll, user)
	
	elif object_is_opinion:
		opinion = comment.opinion
		comment_dictt['opinion'] = compile_opinion_details(request, opinion, user)
	
	if request.user: 
		comment_dictt['hasSharedComment'] = comment.id in return_comments_shared(request, user)
	return comment_dictt