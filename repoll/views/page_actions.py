from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import transaction
from sqlalchemy.exc import DBAPIError

from ..form import (PollCreateForm,
    LoginForm)

from ..models.main_models import (User,
    Comment,
    Poll,
    Option,
    Category,
    TargetedPolls,
    PollCategory, Activity)

from ..services.follow_service import FollowService

from ..form import RegistrationForm
from pyramid.security import remember, forget

from ..services.follow_service import *


@view_config(route_name="create_page_page", renderer="../templates/create_page.jinja2")
def create_page_page(request):
    return {}


@view_config(route_name="create_new_page", renderer="../templates/create_new_page.jinja2")
def create_new_page(request):
    return {}
