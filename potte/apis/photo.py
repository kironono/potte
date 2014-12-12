# coding: utf-8

from ..models import (
    DBSession,
    Photo,
)


def create_photo(photo_id, filename, username, created_at):
    photo = Photo()
    photo.id = photo_id
    photo.filename = filename
    photo.username = username
    photo.created_at = created_at
    DBSession.add(photo)
    return photo
