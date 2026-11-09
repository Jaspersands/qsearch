#!/bin/sh
# Sequential sweep (one CPU job), niced and time-limited by the caller.
PY=/opt/anaconda3/bin/python
cd "$(dirname "$0")"
P=2147483647
{
for a in 2 3 4 5 6 7 8 9; do $PY merge_tree.py triple $P 2 $a 3; done
for a in 2 3 4 5 6 7 8; do $PY merge_tree.py triple $P 3 $a 3; done
} > merge_triple.out 2>&1
{
for a in 2 4 6 8 10 12; do $PY merge_tree.py pair $P 2 $a 40; done
for a in 2 4 6 8 10; do $PY merge_tree.py pair $P 3 $a 40; done
} > merge_pair.out 2>&1
$PY hybrid_fc.py $P 2 16 3 10 0 2 4 6 8 10 12 14 16 > hybrid_k2.out 2>&1
$PY hybrid_fc.py $P 3 10 3 10 0 2 4 6 8 10 > hybrid_k3.out 2>&1
echo done > run_all.done
