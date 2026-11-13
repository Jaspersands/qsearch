#!/bin/zsh
# usage: capped.sh <timeout_s> <rss_cap_kb> <logfile> cmd...   (runs cmd under nice/timeout, kills it above the RSS cap)
TO=$1; CAP=$2; LOG=$3; shift 3
t0=$(date +%s)
nice -n 19 timeout $TO "$@" > $LOG 2>&1 &
pid=$!; maxrss=0
while kill -0 $pid 2>/dev/null; do
  for q in $pid $(pgrep -P $pid 2>/dev/null) $(pgrep -P $(pgrep -P $pid 2>/dev/null | head -1) 2>/dev/null); do
    r=$(ps -o rss= -p $q 2>/dev/null | tr -d ' '); [[ -n $r && $r -gt $maxrss ]] && maxrss=$r
  done
  if [[ $maxrss -gt $CAP ]]; then pkill -P $pid; kill $pid; echo KILLED_RSS >> $LOG; fi
  sleep 10
done
wait $pid; rc=$?
echo "CAPPED rc=$rc time=$(( $(date +%s)-t0 ))s maxrss_kb=$maxrss" >> $LOG
