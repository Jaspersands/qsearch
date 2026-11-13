#!/bin/zsh
# p = 7 triple with a watchdog: kill if RSS > 1.5 GB or wall time > 60 min (then the cell is NOT computed)
cd "$(dirname "$0")"
nice -n 19 /opt/anaconda3/bin/python pairmeas.py 7 triple 1:0,0:1,1:2 nopgm,nopost > triple_7_a.out 2>&1 &
PID=$!; T0=$(date +%s); MAXRSS=0
while kill -0 $PID 2>/dev/null; do
  R=$(ps -o rss= -p $PID 2>/dev/null | tr -d ' '); R=${R:-0}; (( R > MAXRSS )) && MAXRSS=$R
  if (( R > 1500000 )); then kill $PID; echo "KILLED rss=$R kB (NOT computed)" >> triple_7_a.out; break; fi
  if (( $(date +%s) - T0 > 3600 )); then kill $PID; echo "KILLED time>60min (NOT computed)" >> triple_7_a.out; break; fi
  sleep 5
done
echo "watchdog: max rss ${MAXRSS} kB, wall $(( $(date +%s) - T0 )) s" >> triple_7_a.out
