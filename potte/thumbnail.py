# coding: utf-8

import os
import uuid
import enum
import tempfile
from PIL import Image


class ThumbnailSize(enum.Enum):
    """サムネイルのサイズ
    サイズの数字は長辺のピクセル数を表す
    """
    large = 1280
    middle = 640
    small = 320


def make_thumbnails(sizes, filepath, storage):
    thumbnails = []
    for size in sizes:
        im = Image.open(filepath)
        ratio = size.value / max(im.size)
        new_size = (int(im.size[0] * ratio), int(im.size[1] * ratio))

        im.thumbnail(new_size, Image.ANTIALIAS)

        temp_fd, temp_path = tempfile.mkstemp()
        im.save(temp_path, 'JPEG', quality=100)

        thumb_id = str(uuid.uuid4())
        storage.put(thumb_id, open(temp_path, 'rb'))
        os.close(temp_fd)

        thumbnails.append((size, thumb_id))

    return thumbnails
