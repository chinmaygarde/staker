import logging
from rich.logging import RichHandler
from rich.traceback import install
import click
import secrets
import string
import subprocess

install(show_locals=True)

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
        raise subprocess.CalledProcessError(process.returncode, cmd)


@click.group(help="Manage an Ethereum staking setup.")
def staker():
    pass


@staker.group(help="Management of the execution layer (ETH1).")
def eth1():
    pass


@eth1.command("start", help="Start the execution layer (ETH1).")
def eth1_start():
    log.info("Starting eth1")


@staker.group(help="Utilities used to manage a staking setup.")
def util():
    pass


@util.command(help="Generate a JWT.")
@click.option("--path", help="The path to write the JWT to.", type=str, required=True)
def generate_jwt(path: str):
    # Generate 32 random bytes
    secret_bytes = secrets.token_bytes(32)

    # Convert to lowercase hex
    jwt_hex = secret_bytes.hex()

    # Validation checks
    assert len(secret_bytes) == 32, "Secret must be 32 bytes"
    assert len(jwt_hex) == 64, "Hex string must be 64 chars"
    assert all(c in string.hexdigits for c in jwt_hex), "Invalid hex chars"
    assert jwt_hex == jwt_hex.lower(), "Hex must be lowercase"

    # Write to file without a newline.
    with open(path, "w", newline="") as f:
        f.write(jwt_hex)

    log.info(f"Generated JWT at {path}")


if __name__ == "__main__":
    staker()
