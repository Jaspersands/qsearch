#!/bin/sh
# snapshot_verify.sh : verify a snapshot of a sweep that is still running.
# Copies out/c*.out (dropping each file's possibly incomplete last line), truncates each
# running chunk to (lo, last p reached], and runs verify_hi.py on it.  While it runs, one
# sweep process is paused (SIGSTOP/SIGCONT) so that at most 4 of our processes compute.
# Output: snapshots/verify_snap_<time>.out
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-t1-sweep-hi
cd "$D" || exit 1
T=$(date +%Y%m%d_%H%M%S); S=snapshots/snap_$T; mkdir -p $S
for f in out/c*.out; do sed '$d' $f > $S/$(basename $f); grep -q '^DONE' $f && cp $f $S/$(basename $f); done
cp out/retry_w*.out $S/ 2>/dev/null
: > $S/chunks_snap.txt
for f in $S/c*.out; do
  n=$(basename $f .out); lo=$(grep "^$n " chunks.txt | awk '{print $2}'); hi=$(grep "^$n " chunks.txt | awk '{print $3}')
  if grep -q '^DONE' $f; then last=$hi; else last=$(grep '^[A-Z]*FOUND' $f | tail -1 | sed 's/.* p=\([0-9]*\) .*/\1/'); fi
  [ -n "$last" ] && echo "$n $lo $last" >> $S/chunks_snap.txt
done
PID=$(pgrep -f famsym_direct | head -1)
N=$(pgrep -f famsym_direct | wc -l)
[ "$N" -ge 4 ] && kill -STOP $PID
/opt/anaconda3/bin/python verify_hi.py 8388608 117441563 $S/chunks_snap.txt $S/c*.out $(ls $S/retry_w*.out 2>/dev/null) > snapshots/verify_snap_$T.out 2>&1
[ "$N" -ge 4 ] && kill -CONT $PID
rm -f $S/c*.out $S/retry_w*.out
tail -25 snapshots/verify_snap_$T.out
