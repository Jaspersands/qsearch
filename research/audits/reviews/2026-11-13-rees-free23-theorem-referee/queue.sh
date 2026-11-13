#!/bin/sh
# sequential, one heavy process at a time
cd "$(dirname "$0")"
nice -n 19 /opt/anaconda3/bin/python e2e.py 11 40 101 > e2e_11.out 2>&1
nice -n 19 /opt/anaconda3/bin/python e2e.py 7 15 202 > e2e_7.out 2>&1
nice -n 19 /opt/anaconda3/bin/python e2e.py 13 10 303 > e2e_13.out 2>&1
