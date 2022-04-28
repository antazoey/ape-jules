import curses
import json
import random
import shutil
import time
from pathlib import Path

import click
from ape import config
from ape.cli import (
    Abort,
    NetworkBoundCommand,
    account_option,
    ape_cli_context,
    contract_option,
    network_option,
)
from ape.cli.options import _load_contracts
from ape.managers.config import CONFIG_FILE_NAME
from rich import print as echo_rich_text
from rich.tree import Tree


def _short_help() -> str:
    return config.get_config("jules")["message"]


@click.group(short_help=_short_help())
def cli():
    pass


@cli.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
def ping(cli_ctx, network):
    """
    Test the connection the network.
    """
    if not network:
        raise Abort("Not connected.")

    ecosystem_name = cli_ctx.provider.network.ecosystem.name
    network_name = cli_ctx.provider.network.name
    provider_name = cli_ctx.provider.name
    click.echo(f"Current connected to :{ecosystem_name}:{network_name}:{provider_name}'.")


@cli.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
@account_option()
def balance(cli_ctx, network, account):
    """
    Check the balance of an account
    """
    _ = network
    amount = cli_ctx.provider.get_balance(account.address)
    output = f"{amount / 10 ** 16} ETH"
    click.echo(output)


@cli.command()
@click.argument("contract", callback=_load_contracts)
def abi(contract):
    """
    Dump the ABI of the given contract.
    """
    abi_dict = {"abi": [abi.dict() for abi in contract.abi]}
    output = json.dumps(abi_dict, indent=4)
    click.echo(output)


@cli.command()
@ape_cli_context()
@contract_option(help="The name of the contract to check.", multiple=True)
def list_ext(cli_ctx, contract):
    """
    List each extension for each of the given contracts.
    """
    extensions = []
    if not contract:
        cli_ctx.abort("There are no contract in this project.")

    for con in contract:
        ext = str(con.sourceId).split(".")[-1]
        extensions.append(ext)

    ext_out = ", ".join(extensions)
    click.echo(f"The given contracts have the following extensions: {ext_out}")


@cli.command(cls=NetworkBoundCommand)
@click.argument("block_id", default="latest", required=False)
@network_option()
def get_block(network, block_id):
    """
    Get a block.
    """
    block = networks.active_provider.get_block(block_id)
    click.echo(block)


@cli.command(cls=NetworkBoundCommand)
@account_option()
@network_option()
def nonce(account, network):
    """
    Get an account nonce.
    """
    _nonce = networks.active_provider.get_nonce(account.address)
    click.echo(_nonce)


@cli.command()
@ape_cli_context()
@click.option("--limit", help="Limit the amount of accounts to list.", default=20)
def test_accounts(cli_ctx, limit):
    """Show all the test account key-pairs."""

    index = 0
    for acct in cli_ctx.account_manager.test_accounts:
        if index < limit:
            bold_addr = click.style(acct.address, bold=True)
            bold_key = click.style(acct.private_key, bold=True)
            acct_text = f"{index}.\npublic_key = {bold_addr}'\nprivate_key = {bold_key}\n"
            click.echo(acct_text)
            index += 1


@cli.command()
@ape_cli_context()
def data_path(cli_ctx):
    """Print the data path."""
    click.echo(cli_ctx.config_manager.DATA_FOLDER)


@cli.command()
@ape_cli_context()
def list_dependencies(cli_ctx):
    """List the downloaded dependencies."""

    folder = cli_ctx.config_manager.DATA_FOLDER / "packages"
    if not folder.exists():
        return

    packages = [p for p in folder.iterdir() if p.is_dir()]
    for package in packages:
        package_tree = Tree(package.name)
        versions = [v for v in package.iterdir() if v.is_dir()]
        for version in versions:
            version_tree = Tree(version.name)
            package_tree.add(version_tree)

        echo_rich_text(package_tree)


@cli.command(cls=NetworkBoundCommand)
@network_option()
@ape_cli_context()
def poll_blocks(cli_ctx, network):
    """
    Launch a deamon process that polls new blocks.
    """
    for new_block in cli_ctx.chain_manager.blocks.poll_blocks():
        click.echo(
            f"New block found: number={new_block.number}, "
            f"timestamp={new_block.timestamp}, "
            f"size={new_block.size}"
        )


@cli.command(cls=NetworkBoundCommand)
@network_option()
@ape_cli_context()
@click.option("--contract-type", help="The contract type containing the event type.", required=True)
@click.option("--contract-address", help="The address of the deployed contract.", required=True)
@click.option("--event-type", help="The type of event to get logs for.", required=True)
def poll_logs(cli_ctx, network, contract_type, contract_address, event_type, required=True):
    """
    Poll new logs from a contract event.
    """
    contract_type = cli_ctx.project_manager.get_contract(contract_type)
    contract_instance = contract_type.at(contract_address)
    event_type = getattr(contract_instance, event_type)

    for new_log in event_type.poll_logs():
        click.echo(new_log.data)


@cli.command()
@ape_cli_context()
def clean(cli_ctx):
    """Delete caches."""

    build_cache = Path.cwd() / ".build"
    contracts_cache = cli_ctx.project_manager.contracts_folder / ".cache"
    packages_cache = cli_ctx.config_manager.DATA_FOLDER / "packages"
    caches = [c for c in (build_cache, contracts_cache, packages_cache) if c.exists()]

    for cache in caches:
        click.echo(f"Deleting {cache}...")
        shutil.rmtree(str(cache))


@cli.command()
@ape_cli_context()
@click.option("--generic", is_flag=True)
def project_structure(cli_ctx, generic):
    """List an example ape project structure"""

    if generic:
        root_tree = Tree("project-name/")
        trees = ["contracts/", "tests/", "scripts/", CONFIG_FILE_NAME]
    else:
        root_tree = Tree(f"{cli_ctx.project_manager.path.name}/")
        trees = [
            f"{cli_ctx.project_manager._project.contracts_folder.name}/",
            f"{cli_ctx.project_manager.tests_folder.name}/",
            f"{cli_ctx.project_manager.scripts_folder.name}/",
            CONFIG_FILE_NAME,
        ]

    for tree in trees:
        root_tree.add(Tree(tree))

    echo_rich_text(root_tree)


@cli.command()
def play_snake():
    """
    Play a game of Snake.
    """

    # initialize screen
    sc = curses.initscr()
    h, w = sc.getmaxyx()
    win = curses.newwin(h, w, 0, 0)

    win.keypad(1)
    curses.curs_set(0)

    # Initial Snake and Apple position
    snake_head = [10, 15]
    snake_position = [[15, 10], [14, 10], [13, 10]]
    apple_position = [20, 20]
    score = 0

    # display apple
    win.addch(apple_position[0], apple_position[1], curses.ACS_DIAMOND)

    prev_button_direction = 1
    button_direction = 1
    key = curses.KEY_RIGHT

    def collision_with_apple(score):
        apple_position = [random.randint(1, h - 2), random.randint(1, w - 2)]
        score += 1
        return apple_position, score

    def collision_with_boundaries(snake_head):
        if (
            snake_head[0] >= h - 1
            or snake_head[0] <= 0
            or snake_head[1] >= w - 1
            or snake_head[1] <= 0
        ):
            return 1
        else:
            return 0

    def collision_with_self(snake_position):
        snake_head = snake_position[0]
        if snake_head in snake_position[1:]:
            return 1
        else:
            return 0

    a = []
    while True:
        win.border(0)
        win.timeout(100)

        next_key = win.getch()

        if next_key == -1:
            key = key
        else:
            key = next_key

        # 0-Left, 1-Right, 3-Up, 2-Down
        if key == curses.KEY_LEFT and prev_button_direction != 1:
            button_direction = 0
        elif key == curses.KEY_RIGHT and prev_button_direction != 0:
            button_direction = 1
        elif key == curses.KEY_UP and prev_button_direction != 2:
            button_direction = 3
        elif key == curses.KEY_DOWN and prev_button_direction != 3:
            button_direction = 2
        else:
            pass

        prev_button_direction = button_direction

        # Change the head position based on the button direction
        if button_direction == 1:
            snake_head[1] += 1
        elif button_direction == 0:
            snake_head[1] -= 1
        elif button_direction == 2:
            snake_head[0] += 1
        elif button_direction == 3:
            snake_head[0] -= 1

        # Increase Snake length on eating apple
        if snake_head == apple_position:
            apple_position, score = collision_with_apple(score)
            snake_position.insert(0, list(snake_head))
            a.append(apple_position)
            win.addch(apple_position[0], apple_position[1], curses.ACS_DIAMOND)

        else:
            snake_position.insert(0, list(snake_head))
            last = snake_position.pop()
            win.addch(last[0], last[1], " ")

        # display snake
        win.addch(snake_position[0][0], snake_position[0][1], "#")

        # On collision kill the snake
        if collision_with_boundaries(snake_head) == 1 or collision_with_self(snake_position) == 1:
            break

    sc.addstr(10, 30, "Your Score is:  " + str(score))
    sc.refresh()
    time.sleep(2)
    curses.endwin()
    click.echo(a)
    click.echo(w, h)
