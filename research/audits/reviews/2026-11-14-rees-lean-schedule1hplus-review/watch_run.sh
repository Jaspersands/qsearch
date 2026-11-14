#!/bin/zsh
# usage: watch_run.sh LOG cmd...   runs cmd (nice 19), kills it if any descendant 'lean' exceeds 3.9 GB RSS; logs peak.
LOG=$1; shift
nice -n 19 /usr/bin/time -l "$@" > $LOG 2>&1 &
PID=$!
PEAK=0
while kill -0 $PID 2>/dev/null; do
  for lp in $(pgrep -f "(^|/)lean .*(Schedule1HPlusReview|claude-501.*scratchpad)") $(pgrep -f "lake build Formal") ; do
    R=$(ps -o rss= -p $lp 2>/dev/null | tr -d ' ')
    [[ -n $R ]] && (( R > PEAK )) && PEAK=$R
    if [[ -n $R ]] && (( R > 3900000 )); then echo "KILLED: rss $R kB" >> $LOG.watch; pkill -P $PID; kill $PID; pkill -f "(^|/)lean .*(Schedule1HPlusReview|claude-501.*scratchpad)"; fi
  done
  sleep 1
done
echo "peak_sampled_kB $PEAK" >> $LOG.watch
