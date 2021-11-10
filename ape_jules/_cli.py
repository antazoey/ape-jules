import json

import click

from ape import networks
from ape.cli import network_option, NetworkBoundCommand
from eth_typing import ChecksumAddress, HexAddress, HexStr


def _abi_callback(arg):
    try:
        file_json = json.load(arg)
        if "abi" in file_json:
            return file_json["abi"]

        return file_json
    except Exception:
        raise click.BadOptionUsage("Was not given a proper ABI JSON file.")


address_option = click.option(
    "--address",
    callback=lambda ctx, param, arg: ChecksumAddress(HexAddress(HexStr(arg))),
    help="The contract address",
    required=True,
)
abi_option = click.option(
    "--abi",
    type=click.File(),
    callback=lambda ctx, param, arg: _abi_callback(arg),
    help="The contract ABI",
    required=True,
)


@click.group()
def cli():
    """Jules's custom Ethereum tools"""


@cli.command(cls=NetworkBoundCommand)
@network_option()
def test_network(network):
    click.echo(f"Currently connected to {networks.active_provider.name}")
