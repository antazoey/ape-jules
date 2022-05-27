# ape-jules

This project is a place to put my custom `ape` commands.

The nature of my own commands:

* Automating / aiding development
* Manual testing
* 3rd party demo plugin
* Experimenting

Everything in this repo is subject to change at any time and will not be versioned!

## Commands

```
  abi                Dump the ABI of the given contract.
  balance            Check the balance of an account
  block              Get a block.
  data-path          Print the data path.
  list-dependencies  List the downloaded dependencies.
  list-ext           List each extension for each of the given contracts.
  nonce              Get an account nonce.
  ping               Test the connection the network.
  refresh            Delete the .ape data folder.
  test-accounts      Print all the test accounts.
  projects           Manage smart-contract projects.
```

## Plugin

### Config

Jules Config variables:

| name     | default       | description                      |
|:--------:|:-------------:|:--------------------------------:|
| message  | "Jules hacks" | Used as the CLI group short help |
