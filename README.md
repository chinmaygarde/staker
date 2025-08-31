# Staker

A solo home staking setup for Ethereum.

There are other projects similar to this one that make the process of solo staking more turnkey. This is just a collection of scripts I use and is not meant to be general purpose.

## Requirements

- A Linux or macOS machine. Either arm64 or amd64 is fine.
- **Docker**: For containerized deployment.
- **Just**: A task runner.
- **UV**: For managing python projects.
- **Git**: For cloning and managing the repository.

## Prerequisites

- Make sure you have installed all the software in the [requirements](#requirements) section.
- Populate a `.env` file file with the environment variables describing the setup. All variables are mandatory.
  - `STAKER_CHAIN_NAME`: The chain name (`mainnet`, `hoodi`)
  - `STAKER_SUGGESTED_FEE_RECIPIENT_ADDRESS`: The fee recipient to use when setting up the beacon chain.
  - `STAKER_DATA_DIR`: The directory used by the containers to store their contents. If its a relative directory, it must start with "./".

## Launching

- `just launch`: Builds docker images and launches the containers.

## Notes

- Use compounding accounts (0x02 type) for validators.
- Use [execution-layer initiated withdrawals](https://hoodi.launchpad.ethereum.org/en/withdrawals) (added with EIP-7002 in Pectra) instead of initiating them via a voluntary broadcast message from a validator.
- There must be a 27.3 hour gap between activation and exit. This may cause some head scratching when testing on a testnet.
