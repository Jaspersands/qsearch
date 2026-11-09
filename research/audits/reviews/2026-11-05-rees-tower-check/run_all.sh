#!/bin/sh
# Commands behind the outputs in this folder (tower checker, 2026-11-05).
# Run from this folder, at most two at a time, under nice -n 10.
PY=/opt/anaconda3/bin/python
$PY thresholds_check.py > thresholds_check.out
./run_towers.sh                      # -> towers_A.out, towers_B.out
$PY witness_check.py witnesses > witnesses.out
$PY witness_check.py uncovered 4,5,6 > uncovered.out
$PY witness_check.py uncovered 8 > uncovered_k8.out
$PY witness_check.py uncovered 9 > uncovered_k9.out
for a in "4 2 3000" "6 3 3000" "8 4 6000" "4 2 6000 8" "6 2 12100" "16 8 51000" "9 3 135000"; do
  $PY tower_check.py excset $a; done > excsets.out
$PY union_e2e.py > union_e2e.out
# negative_control.out and step1_control.out: inline snippets recorded in the check report, Section 3.
