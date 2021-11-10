import json

import click

from ape import networks
from ape.cli import network_option, NetworkBoundCommand


@click.group()
def cli():
    """Jules's custom Ethereum tools"""


@cli.command(cls=NetworkBoundCommand)
@network_option()
def test_network(network):
    click.echo(f"Currently connected to {networks.active_provider.name}")
