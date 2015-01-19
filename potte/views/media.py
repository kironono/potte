# coding: utf-8

import os
import mimetypes

from pyramid.view import view_config
from pyramid.security import Authenticated
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse

from ..apis.photo import get_photo_by_id, get_photo_store_filepath, \
    get_thumbnail, get_thumbnail_store_filepath


@view_config(route_name='media_photo_original',
             effective_principals=Authenticated)
def media_photo_original_view(request):
    photo_id = request.matchdict['photo_id']
    photo = get_photo_by_id(photo_id)
    if not photo:
        raise HTTPNotFound()

    content_type, content_encoding = mimetypes.guess_type(
        photo.filename, strict=False)
    if content_type:
        content_type = str(content_type)
    filepath = get_photo_store_filepath(photo, request)
    if not os.path.exists(filepath):
        raise HTTPNotFound(request.url)

    return FileResponse(filepath, request, content_type=content_type,
                        cache_max_age=3600)


@view_config(route_name='media_photo_thumbnail',
             effective_principals=Authenticated)
def media_photo_thumbnail_view(request):
    photo_id = request.matchdict['photo_id']
    size_name = request.matchdict['size']

    thumbnail = get_thumbnail(photo_id, size_name)
    if not thumbnail:
        raise HTTPNotFound()

    filepath = get_thumbnail_store_filepath(thumbnail, request)
    if not os.path.exists(filepath):
        raise HTTPNotFound(request.url)

    return FileResponse(filepath, request, content_type='image/jpeg',
                        cache_max_age=3600)
