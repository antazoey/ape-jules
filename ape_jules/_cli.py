import json
import shutil

import click
from ape import accounts, config, networks
from ape.cli import (
    NetworkBoundCommand,
    account_option_that_prompts_when_not_given,
    network_option, contract_option,
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


@cli.command()
@contract_option(help="The name of the contract to get events for.")
def abi(contract):
    """
    Dump the ABI of the given contract.
    """
    abi_dict = {"abi": [abi.to_dict() for abi in contract.abi]}
    output = json.dumps(abi_dict, indent=4)
    click.echo(output)


@cli.command()
@contract_option(help="The name of the contract to get events for.", multiple=True)
def list_ext(contract):
    """
    List each extension for each of the given contracts.
    """
    extensions = []
    for con in contract:
        ext = str(con.sourceId).split(".")[-1]
        extensions.append(ext)

    ext_out = ", ".join(extensions)
    click.echo(f"The given contracts have the following extensions: {ext_out}")


@cli.command(cls=NetworkBoundCommand)
@click.argument("block_id", default="latest", required=False)
@network_option()
def block(network, block_id):
    """
    Get a block.
    """
    b = networks.active_provider._web3.eth.get_block(block_id).keys()
    b = [k for k in b]
    click.echo(b)


@cli.command(cls=NetworkBoundCommand)
@account_option_that_prompts_when_not_given()
@network_option()
def nonce(account, network):
    """
    Get an account nonce.
    """
    _nonce = networks.active_provider.get_nonce(account.address)
    click.echo(_nonce)


@cli.command()
@click.option("--limit", help="Limit the amount of accounts to list.", default=20)
def test_accounts(limit):
    def _yield_accounts():
        index = 0
        for acct in accounts.test_accounts:
            if index < limit:
                bold_addr = click.style(acct.address, bold=True)
                bold_key = click.style(acct._private_key, bold=True)
                acct_text = f"{index}:\n\taddress='{bold_addr}'\n\tprivate_key='{bold_key}'\n-------"
                yield acct_text
                index += 1

    click.echo_via_pager(_yield_accounts())


@cli.command()
def clean():
    """
    Delete the .ape data folder.
    """
    folder = config.DATA_FOLDER
    shutil.rmtree(folder)
