# coding: utf-8

import click
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from potte.models import initialize_sql
from potte.apis.user import (
    get_by_username,
    list_users,
    create_user,
    delete_user,
)


def _initialize(config_uri):
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    initialize_sql(settings)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('config_uri', type=click.Path(exists=True))
def list(config_uri):
    _initialize(config_uri)

    users = list_users()
    if not users:
        click.echo("User not found.")
        return

    click.echo("Username\tEmail")
    for user in users:
        click.echo("{0.username}\t{0.email}".format(user))


@cli.command()
@click.argument('config_uri', type=click.Path(exists=True))
@click.option('--username', prompt='Username')
@click.option('--email', prompt='Email')
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def add(config_uri, username, email, password):
    _initialize(config_uri)

    if get_by_username(username):
        click.echo("User exists: %s" % username)
        return

    with transaction.manager:
        create_user(username, email, password)

    click.echo("User created")


@cli.command()
@click.argument('config_uri', type=click.Path(exists=True))
@click.option('--username', prompt='Username')
def delete(config_uri, username):
    _initialize(config_uri)

    if not get_by_username(username):
        click.echo("User not exists: %s" % username)
        return

    with transaction.manager:
        delete_user(username)

    click.echo("User deleted")
