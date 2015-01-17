# coding: utf-8

from ..models import (
    DBSession,
    Photo,
)
from ..storage import PhotoStorage


def create_photo(photo_id, filename, username, created_at):
    photo = Photo()
    photo.id = photo_id
    photo.filename = filename
    photo.username = username
    photo.created_at = created_at
    DBSession.add(photo)
    return photo


def get_photo_by_id(photo_id):
    return DBSession.query(Photo).filter_by(id=photo_id).first()


def get_photo_store_filepath(photo, request):
    root_dir = request.registry.settings['potte.photo_store_dir']
    storage = PhotoStorage(root_dir)
    identity = storage.calc_identity(photo.id)
    filepath = storage.get_store_path(identity)
    return filepath
