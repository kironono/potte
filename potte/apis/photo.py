# coding: utf-8

from ..models import (
    DBSession,
    Photo,
    PhotoThumbnail,
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


def create_thumbnail(thumb_id, photo_id, size_name):
    thumb = PhotoThumbnail()
    thumb.id = thumb_id
    thumb.photo_id = photo_id
    thumb.size = size_name
    DBSession.add(thumb)
    return thumb


def list_photos(username):
    return DBSession.query(Photo).filter_by(username=username).all()


def count_photos(username):
    return DBSession.query(Photo).filter_by(username=username).count()


def get_photo(photo_id, username):
    return DBSession.query(Photo).filter_by(id=photo_id) \
        .filter_by(username=username).first()


def get_photo_by_id(photo_id):
    return DBSession.query(Photo).filter_by(id=photo_id).first()


def get_photo_store_filepath(photo, request):
    root_dir = request.registry.settings['potte.photo_store_dir']
    storage = PhotoStorage(root_dir)
    identity = storage.calc_identity(photo.id)
    filepath = storage.get_store_path(identity)
    return filepath


def get_thumbnail(photo_id, size_name):
    return DBSession.query(PhotoThumbnail).filter_by(photo_id=photo_id) \
        .filter_by(size=size_name).first()


def get_thumbnail_store_filepath(thumbnail, request):
    root_dir = request.registry.settings['potte.thumbnail_store_dir']
    storage = PhotoStorage(root_dir)
    identity = storage.calc_identity(thumbnail.id)
    filepath = storage.get_store_path(identity)
    return filepath
