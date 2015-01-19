# coding: utf-8


def includeme(config):

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('dashboard', '/')
    config.add_route('upload', '/upload')
    config.add_route('upload_file', '/upload/file')
    config.add_route('albums', '/albums')
    config.add_route('album', '/album/{album_id}')
    config.add_route('album_edit', '/album/{album_id}/edit')
    config.add_route('album_delete', '/album/{album_id}/delete')
    config.add_route('photos', '/photos')
    config.add_route('photo', '/photo/{photo_id}')
    config.add_route('photo_edit', '/photo/{photo_id}/edit')
    config.add_route('photo_delete', '/photo/{photo_id}/delete')

    config.add_route('media_photo_original', '/media/photo/{photo_id}/original')
    config.add_route('media_photo_thumbnail', '/media/thumbnail/{photo_id}/{size}')

    config.add_route('user', '/{username}')
    config.add_route('user_albums', '/{username}/albums')
    config.add_route('user_album', '/{username}/album/{album_id}')
    config.add_route('user_photo', '/{username}/photo/{photo_id}')
