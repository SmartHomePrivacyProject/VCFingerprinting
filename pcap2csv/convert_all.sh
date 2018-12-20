#!/bin/bash
# Edit to switch IP address and correct pcap path

# for f in raw_pcap/amazon_echo/*.pcap; do
#   pcap_2_csv "$f" 192.168.86.40
# done

for f in raw_pcap/amazon_echo/*.pcap; do
  python3 pcap_2_csv.py "$f" 192.168.86.40
done