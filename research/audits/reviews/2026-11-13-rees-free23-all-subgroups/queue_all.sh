#!/bin/sh
# waits for queue_spoiled.sh, then runs the all-types end-to-end simulation; one heavy process at a time
cd "$(dirname "$0")"
while pgrep -f e2e_spoiled.py > /dev/null; do sleep 10; done
nice -n 19 /opt/anaconda3/bin/python hsp_all.py 7 4 707 > hsp_all_7.out 2>&1
nice -n 19 /opt/anaconda3/bin/python hsp_all.py 11 4 1111 > hsp_all_11.out 2>&1
nice -n 19 /opt/anaconda3/bin/python hsp_all.py 13 3 1313 > hsp_all_13.out 2>&1
