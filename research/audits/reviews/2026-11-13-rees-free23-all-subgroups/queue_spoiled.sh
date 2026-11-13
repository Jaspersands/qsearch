#!/bin/sh
# sequential, one heavy process at a time (< 0.4 GB RSS)
cd "$(dirname "$0")"
nice -n 19 /opt/anaconda3/bin/python e2e_spoiled.py 5 150 501 > e2e_spoiled_5.out 2>&1
nice -n 19 /opt/anaconda3/bin/python e2e_spoiled.py 7 40 502 > e2e_spoiled_7.out 2>&1
