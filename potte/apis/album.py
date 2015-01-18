# coding: utf-8

from ..models import (
    DBSession,
    Album,
)


def list_albums(username):
    return DBSession.query(Album).filter_by(username=username).all()


def count_albums(username):
    return DBSession.query(Album).filter_by(username=username).count()


def get_album(album_id, username):
    return DBSession.query(Album).filter_by(id=album_id) \
        .filter_by(username=username).first()


def create_album(album_id, album_name, username, created_at):
    album = Album()
    album.id = album_id
    album.name = album_name
    album.username = username
    album.created_at = created_at
    DBSession.add(album)
    return album
