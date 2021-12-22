import sys

from ape import accounts
from ape.utils import notify
from ape_ledger.accounts import LedgerAccount
from eth_account.messages import encode_structured_data


# Script Parameters
ACCOUNT_ALIAS = "ledger2"

# Script "constants"
DATA = {
    "domain": {
        "chainId": 1,
        "name": "Ether Mail",
        "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
        "version": "1",
    },
    "message": {
        "contents": "Hello, Bob!",
        "from": {
            "name": "Cow",
            "wallets": [
                "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826",
                "0xDeaDbeefdEAdbeefdEadbEEFdeadbeEFdEaDbeeF",
            ],
        },
        "to": [
            {
                "name": "Bob",
                "wallets": [
                    "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB",
                    "0xB0BdaBea57B0BDABeA57b0bdABEA57b0BDabEa57",
                    "0xB0B0b0b0b0b0B000000000000000000000000000",
                ],
            },
        ],
    },
    "primaryType": "Mail",
    "types": {
        "address": [],
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "Group": [
            {"name": "name", "type": "string"},
            {"name": "members", "type": "Person[]"},
        ],
        "Mail": [
            {"name": "from", "type": "Person"},
            {"name": "to", "type": "Person[]"},
            {"name": "contents", "type": "string"},
        ],
        "Person": [
            {"name": "name", "type": "string"},
            {"name": "wallets", "type": "address[]"},
        ],
    },
}


def main():
    account = _load_account()
    message = encode_structured_data(primitive=DATA)

    print("Signing using Ledger device, Please follow the prompts on the device\n...")
    signature = account.sign_message(message)
    notify("SUCCESS", f"Message signed: {signature}")


def _load_account():
    """
    Loads the Ledger account using the script alias parameter.
    Raises errors if it does not find the account or the account is not actually a Ledger account.
    """

    try:
        account = accounts.load(ACCOUNT_ALIAS)
    except IndexError:
        print(
            f"No existing account with name {ACCOUNT_ALIAS}. Set it accordingly at the top of the script."
        )
        sys.exit(1)

    if not isinstance(account, LedgerAccount):
        print(f"Account with alias '{ACCOUNT_ALIAS}' is not a Ledger account.")
        print("Please use a Ledger account for this demo.")
        sys.exit(1)

    return account


if __name__ == "__main__":
    main()
