import click
from ape import config, networks
from ape.cli import (
    NetworkBoundCommand,
    account_option_that_prompts_when_not_given,
    network_option,
)


@click.group(short_help=config.get_config("jules")["message"])
def cli():
    pass


@cli.command(cls=NetworkBoundCommand)
@network_option()
def ping(network):
    """
    Test the connection the network
    """
    _ = network
    click.echo(f"Currently using a(n) {networks.active_provider.name} network.")


@cli.command(cls=NetworkBoundCommand)
@network_option()
@account_option_that_prompts_when_not_given()
def balance(network, account):
    """
    Check the balance of an account
    """
    _ = network
    amount = networks.active_provider.get_balance(account.address)
    click.echo(amount)
