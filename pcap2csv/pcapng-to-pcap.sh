#!/bin/bash
# Replace file extensions with pcap

for f in *.pcapng; 
    do mv $f `basename $f .pcapng`.pcap;
done;
