#!/bin/zsh
# General version of run_split.sh: k dependencies, arbitrary S. Each line of the case file (or the
# empty case "-") is split on the slot (direction (1,1), coset 0) over all p^k values of gamma,
# an exact cover of that case. CaDiCaL + lrat-check as in gadget_cnf5.py.
# usage: run_split_k.sh p S k casefile|- jobs outfile
p=$1; S=$2; k=$3; cases=$4; jobs=$5; out=$6
SP=${SCRATCH:?set SCRATCH}
# 9 Nov: the build in a session scratchpad was unsound (it verified an empty clause without a
# conflict); use the fixed build and refuse to start unless it passes its negative controls.
FIXDIR=${0:A:h}/../2026-11-09-lrat-checker-fix
export LRAT_CHECK=${LRAT_CHECK:-$FIXDIR/lrat-check}
$FIXDIR/controls.sh $LRAT_CHECK - > /dev/null || { echo "lrat-check failed its controls: $LRAT_CHECK" >&2; exit 1; }
if [[ $cases == - ]]; then src=(""); else src=("${(@f)$(cat $cases)}"); fi
/opt/anaconda3/bin/python -c "
import itertools,sys
p,k=$p,$k
for c in sys.argv[1:]:
    for g in itertools.product(range(p),repeat=k):
        print((c+';' if c else '')+'1,1,0:'+','.join(map(str,g)))" "${src[@]}" \
 | xargs -P $jobs -I{} /opt/anaconda3/bin/python -B gadget_cnf5.py $p $S $k 2 nest --quiet --work $SP/sat --fix "{}" >> $out 2>&1
echo "DONE $(date)" >> $out
