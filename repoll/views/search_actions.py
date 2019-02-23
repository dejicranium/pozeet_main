from pyramid.view import view_config
from ..models.main_models import User, Poll, Opinion, Comment, Reply
from pyramid.response import Response
import transaction
from pyramid.httpexceptions import HTTPFound

