# coding: utf-8

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import initialize_sql
from .apis.user import auth_groupfinder
from .request import RequestWithUserAttribute


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    initialize_sql(settings)

    config = Configurator(settings=settings)

    config.include('pyramid_tm')
    config.include('pyramid_redis_sessions')
    config.include('pyramid_jinja2')

    config.add_jinja2_search_path('potte:templates/')

    # auth
    authn_policy = AuthTktAuthenticationPolicy(
        settings['authtkt.secret'],
        callback=auth_groupfinder,
        hashalg='sha512',
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # request
    config.set_request_factory(RequestWithUserAttribute)

    config.include('.urls')

    config.scan()
    return config.make_wsgi_app()
