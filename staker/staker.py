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
        raise subprocess.CalledProcessError(process.returncode, ' '.join(cmd))


@click.group(help="Manage an Ethereum staking setup.")
def staker():
    pass


@staker.group(help="Management of the execution layer (ETH1).")
def eth1():
    pass

@staker.group(help="Management of the concensus layer (ETH2).")
def eth2():
    pass

@eth1.command("start", help="Start the execution layer (ETH1).")
@click.option("--chain", type=str, default="hoodi")
@click.option("--jwt-path", type=str, required=True)
@click.option("--host", type=str, default="0.0.0.0")
@click.option("--port", type=int, default=8551)
@click.option("--data-dir", type=str, required=True)
def eth1_start(chain: str, jwt_path: str, host: str, port: int, data_dir: str):
    run_command([
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
    ])


@eth2.command("start", help="Start the concensus layer (ETH2).")
@click.option("--chain", type=str, default="hoodi")
@click.option("--eth1-url", type=str, required=True)
@click.option("--jwt-path", type=str, required=True)
@click.option("--data-dir", type=str, required=True)
def eth2_start(chain: str, eth1_url: str, jwt_path: str, data_dir: str):
    run_command([
        "lighthouse",
        "beacon_node",
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
    ])

@staker.group(help="Utilities used to manage a staking setup.")
def util():
    pass


@util.command(help="Generate a JWT.")
@click.option("--jwt-path", help="The path to write the JWT to.", type=str, required=True)
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
