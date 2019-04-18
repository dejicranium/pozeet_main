from ..models.main_models import PollVotes

def map_user_poll_option(request, user_id, poll_id,  option_id ):
    """
    This ensures that we save to our UserPollVotes the exact option that a user voted for in a poll

    :param request: Pyramid Request object
    :param user_id: the id of the user who is voting
    :param poll_id: the id of poll being voted on
    :param option_id: the id of the poll that the user is voting for.
    :return: null
    """

    new_user_poll_vote = PollVotes()
    new_user_poll_vote.user_id  = user_id
    new_user_poll_vote.poll_id =  poll_id
    new_user_poll_vote.option_id = option_id

    # add to database
    request.dbsession.add(new_user_poll_vote)
    request.dbsession.flush()

    return new_user_poll_vote

