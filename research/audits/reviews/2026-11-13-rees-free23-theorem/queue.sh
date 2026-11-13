#!/bin/zsh
# sequential queue (one heavy process at a time), each with a 2 h cap
cd "$(dirname "$0")"
PY=/opt/anaconda3/bin/python
nice -n 19 timeout 7000 $PY theorem_pipeline.py 11 30 11 > tp_11.out 2>&1
nice -n 19 timeout 7000 $PY theorem_pipeline.py 13 6 13 > tp_13.out 2>&1
nice -n 19 timeout 7000 $PY theorem_pipeline.py 17 6 17 > tp_17.out 2>&1
