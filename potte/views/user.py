# coding: utf-8

from pyramid.view import view_config
from pyramid.security import Authenticated
from pyramid.httpexceptions import HTTPNotFound

from ..apis.user import get_by_username


@view_config(route_name='user', effective_principals=Authenticated,
             renderer='user/profile.jinja2')
def user_view(request):
    user = get_by_username(username=request.matchdict['username'])
    if not user:
        raise HTTPNotFound
    return {
        'user': user,
    }
