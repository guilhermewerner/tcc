#!/usr/bin/env bash

sudo tshark -a duration:60 -f "port 25565" -w ./trace/java-60s.pcap
sudo tshark -a duration:60 -f "port 19132" -w ./trace/bedrock-60s.pcap
