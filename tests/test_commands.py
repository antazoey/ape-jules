ZEROTH_PUBLIC_KEY = "0x1e59ce931B4CFea3fe4B875411e280e173cB7A9C"
ZEROTH_PRIVATE_KEY = "0xdd23ca549a97cb330b011aebb674730df8b14acaee42d211ab45692699ab8ba5"
FIRST_PUBLIC_KEY = "0xc89D42189f0450C2b2c3c61f58Ec5d628176A1E7"
FIRST_PRIVATE_KEY = "0xf1aa5a7966c3863ccde3047f6a1e266cdc0c76b399e256b8fede92b1c69e4f4e"


def test_test_accounts(cli, runner):
    result = runner.invoke(cli, ["test-accounts"], catch_exceptions=False)
    assert result.exit_code == 0, result.output

    assert "0." in result.output
    assert f"public_key = {ZEROTH_PUBLIC_KEY}" in result.output
    assert f"private_key = {ZEROTH_PRIVATE_KEY}" in result.output

    assert "1." in result.output
    assert f"public_key = {FIRST_PUBLIC_KEY}" in result.output
    assert f"private_key = {FIRST_PRIVATE_KEY}" in result.output
