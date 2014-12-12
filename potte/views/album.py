# coding: utf-8

from pyramid.view import view_config, view_defaults
from pyramid.security import Authenticated


@view_defaults(route_name='album_new', effective_principals=Authenticated,
               renderer='album/new.jinja2')
class NewAlbumView(object):

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def show_form(self):
        return {}

    @view_config(request_method='POST', check_csrf=True)
    def post_form(self):
        return {}
