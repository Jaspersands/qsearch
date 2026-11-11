#!/bin/zsh
# Solve every case of a case file with int_cnf.py (equi mode, original nondegeneracy), CaDiCaL with an
# LRAT proof checked by the FIXED lrat-check (preflight: its controls.sh must pass).  Proofs are deleted
# after checking.  usage: run_cases_mode.sh p S casefile jobs outfile mode   (mode: equi | freeR | free)
p=$1; S=$2; cases=$3; jobs=$4; out=$5; mode=$6
D=${0:A:h}
SC=${SCRATCH:?set SCRATCH}
FIXDIR=$D/../2026-11-09-lrat-checker-fix
zsh $FIXDIR/controls.sh > /dev/null || { echo "lrat-check failed its controls" >&2; exit 1; }
echo "START $(date) mode=$mode p=$p S=$S cases=$cases ($(wc -l < $cases) lines) controls OK" >> $out
cat -n $cases | xargs -P $jobs -L 1 zsh -c 'nice -n 19 /opt/anaconda3/bin/python -I '$D'/int_cnf.py '$p' '$S' nest '$mode' --fix "$1" --work '$SC'/'$mode'case$0 --tag '$mode'case$0 2>&1 | sed "s/^/case $0: /"' >> $out
echo "DONE $(date)" >> $out
