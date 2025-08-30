FROM debian:latest

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y wget

RUN mkdir ~/downloads
RUN wget -O ~/downloads/reth.tar.gz https://github.com/paradigmxyz/reth/releases/download/v1.6.0/reth-v1.6.0-`uname -m`-unknown-linux-gnu.tar.gz
RUN tar -xzvf ~/downloads/reth.tar.gz -C /usr/local/bin
RUN reth --version

RUN wget -O ~/downloads/lighthouse.tar.gz https://github.com/sigp/lighthouse/releases/download/v7.1.0/lighthouse-v7.1.0-`uname -m`-unknown-linux-gnu.tar.gz
RUN tar -xzvf ~/downloads/lighthouse.tar.gz -C /usr/local/bin
RUN reth --version

RUN rm -rf ~/downloads
