# coding: utf-8

import os
import shutil
import hashlib


class PhotoStorage(object):

    def __init__(self, root, digest="sha1", level=3):
        self.root = root
        self.digest = digest
        self.level = level

    def calc_identity(self, photo_id):
        h = hashlib.new(self.digest)
        h.update(photo_id.encode('utf-8'))
        return h.hexdigest()

    def get_store_path(self, identity):
        tokens = [identity[0:l] for l in range(1, self.level)]
        store_dir = os.path.join(self.root, *tokens)
        store_dir = os.path.normpath(store_dir)
        return os.path.join(store_dir, identity)

    def exists(self, photo_id):
        identity = self.calc_identity(photo_id)
        store_path = self.get_store_path(identity)
        return os.path.exists(store_path)

    def get(self, photo_id):
        identity = self.calc_identity(photo_id)
        store_path = self.get_store_path(identity)
        return open(store_path)

    def put(self, photo_id, file):
        identity = self.calc_identity(photo_id)
        store_path = self.get_store_path(identity)
        store_dir = os.path.dirname(store_path)

        if not os.path.isdir(store_dir):
            os.makedirs(store_dir)

        fd = os.open(store_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        wf = os.fdopen(fd, "wb")
        pos = file.tell()
        shutil.copyfileobj(file, wf)
        file.seek(pos)
        wf.close()
        return identity

    def remove(self, photo_id):
        identity = self.calc_identity(photo_id)
        store_path = self.get_store_path(identity)
        os.remove(store_path)
