FROM ubuntu:22.04

# Noninteractive mode
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    gnuradio \ 
    gr-osmosdr \ 
    rtl-sdr \
    python3-numpy \ 
    python3-scipy \ 
    python3-matplotlib \ 
    python3-rtlsdr \ 
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Create a workspace
WORKDIR /workspace
