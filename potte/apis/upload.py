# coding: utf-8

import datetime
import uuid

from ..storage import PhotoStorage
from .album import get_album, create_album
from .photo import create_photo, create_thumbnail
from ..thumbnail import ThumbnailSize, make_thumbnails


def registration_photo(request, user, album_id, fs):
    album = get_album(album_id, user.username)
    now = datetime.datetime.now()
    if not album:
        album_name = now.strftime("%Y-%m-%d")
        album = create_album(album_id, album_name, user.username, now)

    settings = request.registry.settings
    storage = PhotoStorage(settings['potte.photo_store_dir'])
    thumb_storage = PhotoStorage(settings['potte.thumbnail_store_dir'])

    photo_id = str(uuid.uuid4())
    filepath = storage.put(photo_id, fs.file)

    sizes = list(ThumbnailSize)
    thumbnails = make_thumbnails(sizes, filepath, thumb_storage)

    photo = create_photo(photo_id, fs.filename, user.username, now)
    album.photos.append(photo)
    for size, thumb_id in thumbnails:
        create_thumbnail(thumb_id, photo_id, size.name)

    return (album, photo)
