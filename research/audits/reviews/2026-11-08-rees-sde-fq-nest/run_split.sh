#!/bin/zsh
# Split every unit-direction case of cases<p>.txt further on the slot (direction (1,1), coset 0):
# all p^2 values of gamma_{(1,1)} are enumerated, so the sub-cases cover the case exactly.
# Each sub-case is solved by CaDiCaL; UNSAT is accepted only after lrat-check verifies the proof.
# usage: run_split.sh p S casefile jobs outfile
p=$1; S=$2; cases=$3; jobs=$4; out=$5
SP=${SCRATCH:?set SCRATCH}
# 9 Nov: the build in a session scratchpad was unsound (it verified an empty clause without a
# conflict); use the fixed build and refuse to start unless it passes its negative controls.
FIXDIR=${0:A:h}/../2026-11-09-lrat-checker-fix
export LRAT_CHECK=${LRAT_CHECK:-$FIXDIR/lrat-check}
$FIXDIR/controls.sh $LRAT_CHECK - > /dev/null || { echo "lrat-check failed its controls: $LRAT_CHECK" >&2; exit 1; }
while read c; do
  for x in $(seq 0 $((p-1))); do for y in $(seq 0 $((p-1))); do
    echo "$c;1,1,0:$x,$y"
  done; done
done < $cases | xargs -P $jobs -I{} /opt/anaconda3/bin/python -B gadget_cnf5.py $p $S 2 2 nest --quiet --work $SP/sat --fix "{}" >> $out 2>&1
echo "DONE $(date)" >> $out
