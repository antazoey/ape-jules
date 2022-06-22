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
  clean              Delete caches.
  data-path          Print the data path.
  get-block          Get a block.
  list-dependencies  List the downloaded dependencies.
  list-ext           List each extension for each of the given contracts.
  nonce              Get an account nonce.
  ping               Test the connection the network.
  play-snake         Play a game of Snake.
  poll-blocks        Launch a deamon process that polls new blocks.
  poll-logs          Poll new logs from a contract event.
  project-structure  List an example ape project structure
  projects           Manage smart-contract projects.
  test-accounts      Show all the test account key-pairs.
```

## Config

Jules Config variables:

| name                | default             | description                      |
|:-------------------:|:-------------------:|:--------------------------------:|
| message             | "Jules hacks"       | Used as the CLI group short help |
| projects_directory  | "$HOME/ApeProjects" | The path to your Ape projects    |
| editor              | code                | Your text editor of choice       |
