# coding: utf-8

import uuid
import colander

from pyramid.view import view_config
from pyramid.security import Authenticated
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

from ..forms.upload import PhotoUploadSchema
from ..apis.upload import registration_photo
from ..apis.album import list_albums, get_album


@view_config(route_name='dashboard', renderer='index.jinja2')
def index_view(request):
    return {}


@view_config(route_name='dashboard', effective_principals=Authenticated,
             renderer='mypage/dashboard.jinja2')
def dashboard_view(request):
    return {}


@view_config(route_name='upload', effective_principals=Authenticated,
             request_method='GET', renderer='mypage/upload.jinja2')
def upload_view(request):
    return {
        "album_uuid": str(uuid.uuid4()),
    }


@view_config(route_name='upload_file', effective_principals=Authenticated,
             request_method='POST', renderer='json')
def upload_file_view(request):
    schema = PhotoUploadSchema()
    try:
        data = schema.deserialize(request.params)
    except colander.Invalid:
        raise HTTPBadRequest

    album, photo = registration_photo(
        request, request.user, data['uuid'], data['file'])
    return {
        "album_id": album.id,
        "photo_id": photo.id,
    }


@view_config(route_name='albums', effective_principals=Authenticated,
             renderer='mypage/albums.jinja2')
def albums_view(request):
    albums = list_albums(request.user.username)
    album_count = len(albums)
    return {
        'albums': albums,
        'album_count': album_count,
    }


@view_config(route_name='album', effective_principals=Authenticated,
             renderer='mypage/album.jinja2')
def album_view(request):
    album_id = request.matchdict['album_id']
    album = get_album(album_id, request.user.username)
    if not album:
        raise HTTPNotFound()
    return {
        'album': album,
    }


@view_config(route_name='photos', effective_principals=Authenticated,
             renderer='mypage/photos.jinja2')
def photos_view(request):
    return {}


@view_config(route_name='photo', effective_principals=Authenticated,
             renderer='mypage/photo.jinja2')
def photo_view(request):
    return {}
