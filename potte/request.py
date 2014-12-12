# coding: utf-8

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid

from .apis.user import get_by_username


class RequestWithUserAttribute(Request):

    @reify
    def user(self):
        username = unauthenticated_userid(self)
        if username is not None:
            user = get_by_username(username)
            return user
