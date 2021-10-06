import json

import click

from ape.cli import ape_group, network_option
from ape import networks
from eth_typing import ChecksumAddress, HexAddress, HexStr
import pandas as pd


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
    required=True
)


@ape_group()
def cli():
    """My custom Ethereum tools"""


@cli.command_using_network_option()
@address_option
@abi_option
@click.option("--event-type", multiple=True, help="Limit logs by event type")
@network_option
def logs(address, abi, event_type, network):
    """Get contract logs"""
    provider = networks.active_provider
    events = [dict(e) for e in provider.get_events()]
    for event in events:
        event["topics"] = [provider._web3.toHex(t) for t in event["topics"]]
    columns = "data", "logIndex", "topics"
    df = pd.DataFrame.from_records(
        events, columns=columns, index="logIndex"
    )
    if df.empty:
        click.echo("No logs found.")
        return

    # defaults = {
    #     "orient": "records",
    #     "lines": True,
    #     "index": True,
    #     "default_handler": str,
    # }
    # output = df.to_json(**defaults)
    click.echo_via_pager(df.to_csv())
