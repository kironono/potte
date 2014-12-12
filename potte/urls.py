# coding: utf-8


def includeme(config):

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('dashboard', '/')
    config.add_route('upload', '/upload')
    config.add_route('upload_file', '/upload/file')

    config.add_route('user', '/{username}')
    config.add_route('albums', '/{username}/albums')
    config.add_route('album', '/{username}/album/{album_id}')
    config.add_route('album_new', '/album/new')
    config.add_route('photos', '/{username}/photos')
    config.add_route('photo', '/{username}/photo/{photo_id}')
