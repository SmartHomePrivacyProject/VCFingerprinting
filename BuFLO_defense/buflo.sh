#!/bin/bash
# apply BuFLO on original data
# input: path, size(d), frequency(f), time(T)

for f in csv/*.csv; do
  python3 buflo.py "$f" 1500 50 100
done
