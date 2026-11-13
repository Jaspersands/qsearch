#!/bin/zsh
# sequential queue (one heavy process at a time); each step < 2 h, < 1.5 GB
cd "$(dirname "$0")"
while kill -0 63437 2>/dev/null; do sleep 5; done
PY=/opt/anaconda3/bin/python
nice -n 19 $PY pairmeas.py 5 triple 1:0,0:1,1:2 > triple_5_a.out 2>&1
nice -n 19 $PY kuperberg_check.py 11 2 > kuperberg_check_11.out 2>&1
nice -n 19 $PY pairmeas.py 5 triple 1:0,0:1,1:1 > triple_5_b.out 2>&1
nice -n 19 $PY pairmeas.py 5 triple 1:0,0:1,4:4 > triple_5_bin.out 2>&1
nice -n 19 $PY pairmeas.py 11 pairs 10 > pairs_11_c10.out 2>&1
nice -n 19 $PY pairmeas.py 7 triple 1:0,0:1,1:2 nopgm,nopost > triple_7_a.out 2>&1
echo done > queue.done
