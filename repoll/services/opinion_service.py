from ..models.main_models import OpinionVotes


def map_user_opinion_option(request, user_id, opinion_id, option_id):
    """
    :param request:
    :param user_id:
    :param opinion_id:
    :param option_id:
    :return:
    """

    new_user_opinion_vote = OpinionVotes()
    new_user_opinion_vote.user_id = user_id
    new_user_opinion_vote.opinion_id = opinion_id
    new_user_opinion_vote.option_id = option_id

    # add to database
    request.dbession.add(new_user_opinion_vote)
    request.dbession.flush()

    return new_user_opinion_vote

