#!/bin/sh
# Tower end-to-end runs (tower checker). Two background jobs at most, under nice.
PY=/opt/anaconda3/bin/python
T=tower_check.py
{
echo "## kappa=4 (chain 2,4): below / E_2(4) / above W(4,2)=96.3 and ((k-1)^2+1)^2=100"
$PY $T tower 4 5,13,29 1,2
$PY $T tower 4 17,37,53 1,2,3
$PY $T tower 4 97,101,109,113 1,2,3 desc weil
echo "## kappa=6 chain (3,6): below / E_2(6) max 859 / above W(6,2)=648.8 / above 279936"
$PY $T tower 6 7,13,79,139,223 1,2
$PY $T tower 6 37,859 1,2,3
$PY $T tower 6 661,673,691 1,2,3 desc weil
$PY $T tower 6 279949,279967 1,2 desc weil
echo "## kappa=6 chain (2,6)"
$PY $T tower 6 7,37,61,97,139 1,2 asc
$PY $T tower 6 223,859 1,2,3 asc
echo "## kappa=8 chain (2,4,8): below / known E_2(8) member 11689 / above W(8,2)=2432.9 and 2500"
$PY $T tower 8 17,233,761 1,2
$PY $T tower 8 1553,11689 1,2
$PY $T tower 8 2441,2473,2521,2593 1,2 desc weil
} > towers_A.out 2>&1 &
{
echo "## kappa=9 chain (3,9): below / E_2(9) members / just below and above T_R(9,3)=134723 / above 4q^2k^5=2125764"
$PY $T tower 9 19,433,523 1,2
$PY $T tower 9 271,17911,17929 1,2
$PY $T tower 9 134353,134371 1,2
$PY $T tower 9 134731,134839,134857 1,2
$PY $T tower 9 2125801,2125819 1,2 desc weil
} > towers_B.out 2>&1 &
wait
