import click

from ape import config, networks
from ape.cli import network_option, NetworkBoundCommand


@click.group(short_help=config.get_config("jules")["message"])
def cli():
    pass


@cli.command(cls=NetworkBoundCommand)
@network_option()
def ping(network):
    """Test the connection the network"""
    click.echo(f"Currently connected to {networks.active_provider.name}")
