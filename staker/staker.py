import logging
from rich.logging import RichHandler
from rich.traceback import install
import click
import os
import secrets
import string
import subprocess

install(show_locals=True, suppress=[click])

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

log = logging.getLogger("rich")


def run_command(cmd):
    log.info(f"Running: '{' '.join(cmd)}'")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,  # Line buffering.
    )

    # Stream output as it arrives.
    for line in process.stdout:
        print(line, end="")

    process.wait()

    # Raise exception on failure.
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, " ".join(cmd))


@click.group(help="Manage an Ethereum staking setup.")
def staker():
    pass


@staker.group(help="Utilities used to manage a staking setup.")
def util():
    pass


@staker.group(help="Management of the execution layer (ETH1).")
def eth1():
    pass


@staker.group(help="Management of the concensus layer (ETH2).")
def eth2():
    pass


@staker.group(help="Management of the validator.")
def validator():
    pass


@eth1.command("start", help="Start the execution layer (ETH1).")
@click.option("--chain", type=str, default="hoodi")
@click.option("--jwt-path", type=str, required=True)
@click.option("--host", type=str, default="127.0.0.1")
@click.option("--port", type=int, default=2222)
@click.option("--data-dir", type=str, required=True)
def eth1_start(chain: str, jwt_path: str, host: str, port: int, data_dir: str):
    run_command(
        [
            "reth",
            "node",
            "--chain",
            chain,
            "--authrpc.jwtsecret",
            jwt_path,
            "--authrpc.addr",
            host,
            "--authrpc.port",
            str(port),
            "--datadir",
            data_dir,
        ]
    )


@eth2.command("start", help="Start the concensus layer (ETH2).")
@click.option("--chain", type=str, default="hoodi")
@click.option("--eth1-url", type=str, default="http://127.0.0.1:2222")
@click.option("--jwt-path", type=str, required=True)
@click.option("--data-dir", type=str, required=True)
@click.option("--host", type=str, default="127.0.0.1")
@click.option("--port", type=int, default=3333)
def eth2_start(
    chain: str, eth1_url: str, jwt_path: str, data_dir: str, host: str, port: int
):
    run_command(
        [
            "lighthouse",
            "beacon_node",
            "--staking",
            "--network",
            chain,
            "--checkpoint-sync-url",
            f"https://{chain}.checkpoint.sigp.io",
            "--execution-endpoint",
            eth1_url,
            "--execution-jwt",
            jwt_path,
            "--datadir",
            data_dir,
            "--gui",
            "--http-address",
            host,
            "--http-port",
            str(port),
        ]
    )


@validator.command("start", help="Start the validator client.")
@click.option("--chain", type=str, default="hoodi")
@click.option("--data-dir", type=str, required=True)
@click.option("--eth2-url", type=str, default="http://127.0.0.1:3333")
@click.option("--suggested-fee-recipient", type=str, required=True)
@click.option("--host", type=str, default="127.0.0.1")
@click.option("--port", type=int, default=4444)
def validator_start(
    chain: str,
    data_dir: str,
    eth2_url: str,
    suggested_fee_recipient: str,
    host: str,
    port: int,
):
    run_command(
        [
            "lighthouse",
            "validator_client",
            "--network",
            chain,
            "--datadir",
            data_dir,
            "--beacon-nodes",
            eth2_url,
            "--suggested-fee-recipient",
            suggested_fee_recipient,
            "--enable-doppelganger-protection",
            # This just acknowledges that the traffic is unexcrypted and
            # won't be exposing it to the public internet.
            "--unencrypted-http-transport",
            "--http",
            "--http-address",
            host,
            "--http-port",
            str(port),
        ]
    )


@util.command(help="Generate a JWT.")
@click.option(
    "--jwt-path", help="The path to write the JWT to.", type=str, required=True
)
def generate_jwt(jwt_path: str):
    # Generate 32 random bytes
    secret_bytes = secrets.token_bytes(32)

    # Convert to lowercase hex
    jwt_hex = secret_bytes.hex()

    # Validation checks
    assert len(secret_bytes) == 32, "Secret must be 32 bytes"
    assert len(jwt_hex) == 64, "Hex string must be 64 chars"
    assert all(c in string.hexdigits for c in jwt_hex), "Invalid hex chars"
    assert jwt_hex == jwt_hex.lower(), "Hex must be lowercase"

    os.makedirs(os.path.dirname(jwt_path), exist_ok=True)

    # Write to file without a newline.
    with open(jwt_path, "w", newline="") as f:
        f.write(jwt_hex)

    log.info(f"Generated JWT at {jwt_path}")


if __name__ == "__main__":
    staker()
