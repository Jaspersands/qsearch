#!/bin/sh
# snapshot_verify.sh : verify the part of a running sweep that is contiguous from 20000.
# Takes every finished chunk (marker out/done_cNN: main pass + retries done; c00 = low/),
# then the prefix of the next chunk if that prefix has no NOTFOUND line yet (its last,
# possibly incomplete, line is dropped).  Runs both verifiers on (20000, X_snap].  While
# they run, one sweep process is paused (SIGSTOP/SIGCONT) so that at most 3 of our
# processes compute.  Output: snapshots/snap_<time>.out
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-k9-sweep
OLDD=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-threshold-5
PY=/opt/anaconda3/bin/python
cd "$D" || exit 1
T=$(date +%Y%m%d_%H%M%S); S=snapshots/snap_$T; mkdir -p $S
FILES="$(ls out/dfs2b_*.out 2>/dev/null)"; X=20000; : > $S/chunks_snap.txt
grep -v '^#' chunks.txt | { while read n lo hi np mode; do
  if [ -f out/done_$n ]; then
    if [ "$n" = c00 ]; then FILES="$FILES $(ls low/*.out)"; else FILES="$FILES out/$n.out out/r_$n.out"; fi
    echo "$n $lo $hi" >> $S/chunks_snap.txt; X=$hi; continue
  fi
  if [ -f out/$n.out ]; then
    sed '$d' out/$n.out > $S/$n.out
    last=$(grep 'FOUND' $S/$n.out | tail -1 | sed 's/.* p=\([0-9]*\) .*/\1/')
    if [ -n "$last" ] && ! grep -q '^NOTFOUND' $S/$n.out; then FILES="$FILES $S/$n.out"; echo "$n $lo $last" >> $S/chunks_snap.txt; X=$last; fi
  fi
  break
done
echo "$X" > $S/X; echo "$FILES" > $S/files; }
X=$(cat $S/X); FILES=$(cat $S/files)
PID=$(pgrep -f 'famsym9 9 ' | head -1); N=$(pgrep -f 'famsym9 9 |famsym 9 |famsearch 9 |run_worker.sh.*dfs2b' | wc -l)
[ "$N" -ge 3 ] && [ -n "$PID" ] && kill -STOP $PID
{ echo "snapshot $T: X_snap=$X"; cat $S/chunks_snap.txt
  nice -n 10 $PY verify_k9.py 20000 $X $S/chunks_snap.txt $FILES
  echo "--- old verifier (--zeros) ---"
  nice -n 10 $PY $OLDD/verify_witnesses.py --zeros --cover 9 20001 $X $FILES | cut -c1-3000
} > snapshots/snap_$T.out 2>&1
[ "$N" -ge 3 ] && [ -n "$PID" ] && kill -CONT $PID
rm -f $S/c*.out
tail -14 snapshots/snap_$T.out
