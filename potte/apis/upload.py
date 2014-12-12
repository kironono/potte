# coding: utf-8

import datetime
import uuid

from ..storage import PhotoStorage
from .album import get_album, create_album
from .photo import create_photo


def registration_photo(request, user, album_id, fs):
    album = get_album(album_id, user.username)
    now = datetime.datetime.now()
    if not album:
        album_name = now.strftime("%Y-%m-%d")
        album = create_album(album_id, album_name, user.username, now)

    photo_id = str(uuid.uuid4())
    root_dir = request.registry.settings['potte.photo_store_dir']
    storage = PhotoStorage(root_dir)
    storage.put(photo_id, fs.file)

    photo = create_photo(photo_id, fs.filename, user.username, now)
    album.photos.append(photo)

    return (album, photo)
