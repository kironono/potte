# coding: utf-8

import click

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from potte.models import initialize_sql
from potte.models import Base


@click.command()
@click.argument('config_uri', type=click.Path(exists=True))
def cli(config_uri):
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    initialize_sql(settings)

    Base.metadata.create_all()
