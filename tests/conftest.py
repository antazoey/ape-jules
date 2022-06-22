import pytest
from click.testing import CliRunner

from ape_jules._cli import cli as jules_cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return jules_cli
