# coding: utf-8

import uuid
import colander

from pyramid.view import view_config
from pyramid.security import Authenticated
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

from ..forms.upload import PhotoUploadSchema
from ..apis.upload import registration_photo
from ..apis.album import list_albums, count_albums, get_album
from ..apis.photo import list_photos, count_photos, get_photo


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
    album_count = count_albums(request.user.username)
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
        raise HTTPNotFound(request.url)
    return {
        'album': album,
    }


@view_config(route_name='photos', effective_principals=Authenticated,
             renderer='mypage/photos.jinja2')
def photos_view(request):
    photos = list_photos(request.user.username)
    photo_count = count_photos(request.user.username)
    return {
        'photos': photos,
        'photo_count': photo_count,
    }


@view_config(route_name='photo', effective_principals=Authenticated,
             renderer='mypage/photo.jinja2')
def photo_view(request):
    photo_id = request.matchdict['photo_id']
    photo = get_photo(photo_id, request.user.username)
    if not photo:
        raise HTTPNotFound(request.url)
    return {
        'photo': photo,
    }
