import pytest
from click.testing import CliRunner
from ape._cli import cli

# Note: this test requires ape-infura.


TEST_CONTRACT_JSON = "data/Vault.json"
TESTS_CONTRACT_ADDRESS = "0xA2B5ee9645f6011b2d6E10f750aB47fB455316EE"
TEST_NETWORK = "ethereum:mainnet:infura"


@pytest.fixture
def runner():
    return CliRunner()


def test_logs(runner):
    """This is the same as doing the following from the root repo:

      `ape jules logs -\
      --abi tests/data/Vault.json \
      --address 0xA2B5ee9645f6011b2d6E10f750aB47fB455316EE \
      --network ethereum:mainnet:infura

    """
    command = f"jules logs --abi {TEST_CONTRACT_JSON} --address {TESTS_CONTRACT_ADDRESS} --network {TEST_NETWORK}"
    result = runner.invoke(cli, command.split(" "))
    print(result.output)
