# coding: utf-8

import colander

from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config,
)
from pyramid.security import forget, remember
from pyramid.httpexceptions import HTTPFound

from ..apis.user import (
    get_by_username,
    check_password,
)
from ..forms.auth import LoginSchema


@forbidden_view_config()
def forbidden_view(request):
    return HTTPFound(location=request.route_path('login'))


@view_defaults(route_name='login', renderer='auth/login.jinja2')
class LoginView(object):

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def show_form(self):
        if self.request.user:
            location = self.request.route_path('dashboard')
            return HTTPFound(location=location)
        return {}

    @view_config(request_method='POST', check_csrf=True)
    def post_form(self):
        schema = LoginSchema()
        params = self.request.params
        try:
            data = schema.deserialize(params)
        except colander.Invalid as e:
            return {
                'errors': e.asdict(),
                'values': params,
            }

        user = get_by_username(data.get('username'))
        if not (user and check_password(user, data.get('password'))):
            msg = u"Username or Password invalid."
            errors = {
                'username': msg,
                'password': msg,
            }
            return {
                'errors': errors,
                'values': params,
            }

        headers = remember(self.request, user.username)
        return HTTPFound(location=self.request.route_path('dashboard'),
                         headers=headers)


@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    location = request.route_path('dashboard')
    return HTTPFound(location=location, headers=headers)
