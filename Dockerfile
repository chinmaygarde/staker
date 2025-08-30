FROM debian:latest

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y wget

# Install Reth (ETH1)
RUN mkdir ~/downloads
RUN wget -O ~/downloads/reth.tar.gz https://github.com/paradigmxyz/reth/releases/download/v1.6.0/reth-v1.6.0-`uname -m`-unknown-linux-gnu.tar.gz
RUN tar -xzvf ~/downloads/reth.tar.gz -C /usr/local/bin
RUN reth --version

# Install Lighthouse (ETH2)
RUN wget -O ~/downloads/lighthouse.tar.gz https://github.com/sigp/lighthouse/releases/download/v7.1.0/lighthouse-v7.1.0-`uname -m`-unknown-linux-gnu.tar.gz
RUN tar -xzvf ~/downloads/lighthouse.tar.gz -C /usr/local/bin
RUN reth --version

# Install UV
RUN wget -O ~/downloads/uv.tar.gz https://github.com/astral-sh/uv/releases/download/0.8.14/uv-`uname -m`-unknown-linux-musl.tar.gz
RUN tar -xzvf ~/downloads/uv.tar.gz -C /usr/local/bin --strip-components=1
RUN uv --version

# Install Forge
RUN wget -O ~/downloads/foundry.tar.gz https://github.com/foundry-rs/foundry/releases/download/v1.3.3/foundry_v1.3.3_linux_`uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/'`.tar.gz
RUN tar -xzvf ~/downloads/foundry.tar.gz -C /usr/local/bin
RUN cast --version

RUN rm -rf ~/downloads

COPY staker /code

RUN uv run --directory /code staker.py --help

ENTRYPOINT [ "uv", "run", "--directory", "/code", "staker.py" ]
CMD [ "--help" ]
