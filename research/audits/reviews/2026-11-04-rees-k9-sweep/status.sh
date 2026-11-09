#!/bin/sh
# status.sh : one line per chunk file (primes done, last p, NOTFOUND), worker logs, procs.
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-k9-sweep
cd "$D" || exit 1
date
for f in out/c*.out; do [ -f "$f" ] || continue
  printf "%s lines=%s last=%s notfound=%s %s\n" $f $(grep -c 'FOUND' $f) "$(grep 'FOUND' $f | tail -1 | sed 's/.* p=\([0-9]*\) .*/\1/')" $(grep -c NOTFOUND $f) "$(grep -q ^DONE $f && echo DONE)"; done
for f in out/r_c*.out; do [ -f "$f" ] && printf "%s FOUND=%s UNRESOLVED=%s\n" $f $(grep -c ^FOUND $f) $(grep -c UNRESOLVED $f); done
tail -n 2 out/worker_*.log
ps -Ao pid,ni,stat,etime,command | egrep 'famsym|famsearch|dfs2b 9 [0-9]+ [0-9]+ 4000000000' | grep -v -e grep -e SCREEN -e 'sh -c' | cut -c1-110
