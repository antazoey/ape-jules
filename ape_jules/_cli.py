import curses
import json
import random
from pathlib import Path
import shutil
import time

import click
from ape import accounts, chain, config, networks
from ape.cli import (
    Abort,
    NetworkBoundCommand,
    account_option,
    ape_cli_context,
    contract_option,
    network_option,
)


@click.group(short_help=config.get_config("jules")["message"])
def cli():
    pass


@cli.command(cls=NetworkBoundCommand)
@network_option()
def ping(network):
    """
    Test the connection the network.
    """
    if not network:
        raise Abort("Not connected.")

    provider = networks.active_provider
    ecosystem_name = provider.network.ecosystem.name
    network_name = provider.network.name
    provider_name = provider.name
    click.echo(f"Current connected to :{ecosystem_name}:{network_name}:{provider_name}'.")


@cli.command(cls=NetworkBoundCommand)
@network_option()
@account_option()
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
@click.option("--limit", help="Limit the amount of accounts to list.", default=20)
def test_accounts(limit):
    """
    Print all the test accounts.
    """

    def _yield_accounts():
        index = 0
        for acct in accounts.test_accounts:
            if index < limit:
                bold_addr = click.style(acct.address, bold=True)
                bold_key = click.style(acct._private_key, bold=True)
                acct_text = (
                    f"{index}:\n\taddress='{bold_addr}'\n\tprivate_key='{bold_key}'\n-------"
                )
                yield acct_text
                index += 1

    click.echo_via_pager(_yield_accounts())


@cli.command()
def data_path():
    """
    Print the data path.
    """
    click.echo(config.DATA_FOLDER)


@cli.command()
def refresh():
    """
    Delete the .ape data folder.
    """
    folder = config.DATA_FOLDER
    if folder.exists():
        shutil.rmtree(config.DATA_FOLDER)


@cli.command()
def list_dependencies():
    """
    List the downloaded dependencies.
    """

    folder = config.DATA_FOLDER / "packages"
    if not folder.exists():
        return

    packages = [p for p in folder.iterdir() if p.is_dir()]
    for package in packages:
        click.echo(package.name)


@cli.command(cls=NetworkBoundCommand)
@network_option()
def poll_blocks(network):
    """
    Launch a deamon process that polls new blocks.
    """
    for new_block in chain.blocks.poll_blocks():
        click.echo(
            f"New block found: number={new_block.number}, "
            f"timestamp={new_block.timestamp}, "
            f"size={new_block.size}"
        )


@cli.command()
@ape_cli_context()
def clean(cli_ctx):
    """Delete caches."""

    build_cache = Path.cwd() / ".build"
    contracts_cache = cli_ctx.project.contracts_folder / ".cache"
    packages_cache = config.DATA_FOLDER / "packages"
    caches = [c for c in (build_cache, contracts_cache, packages_cache) if c.exists()]

    for cache in caches:
        click.echo(f"Deleting {cache}...")
        shutil.rmtree(str(cache))


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
