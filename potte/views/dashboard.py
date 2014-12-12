# coding: utf-8

from pyramid.view import view_config
from pyramid.security import Authenticated


@view_config(route_name='dashboard', renderer='index.jinja2')
def index_view(request):
    return {}


@view_config(route_name='dashboard', effective_principals=Authenticated,
             renderer='mypage/dashboard.jinja2')
def dashboard_view(request):
    return {}
