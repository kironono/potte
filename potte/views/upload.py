# coding: utf-8

import logging
import uuid
import colander

from pyramid.view import view_config
from pyramid.security import Authenticated
from pyramid.httpexceptions import HTTPBadRequest

from ..apis.upload import registration_photo
from ..forms.upload import PhotoUploadSchema

log = logging.getLogger(__name__)


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

    album, photo = registration_photo(request, request.user,
                                      data['uuid'], data['file'])
    return {
        "album_id": album.id,
        "photo_id": photo.id,
    }
