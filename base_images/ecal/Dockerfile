FROM ubuntu:24.04

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    software-properties-common \
    git \
    jq \
    python3 \
    python3-pip \
    # install eCAL
    && add-apt-repository ppa:ecal/ecal-5.12 \
    && apt-get install -y python3-ecal5 \
    && rm -rf /var/lib/apt/lists/*
