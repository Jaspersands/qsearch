#!/bin/bash
# Local run of the 2026-11-06 other-device brief (phases 2, 3a, 3b; 143 jobs), resumable.
# Uses the canonical dfs2b binary in small-prime/. Node limit 1e15 (no LIMIT). Never kill.
cd /Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-07-rees-dfs2b-local-queue
N=${JOBS:-8}
one() { k=$1; p=$2; m=$3; f=out/${k}_${p}_${m}.out
  grep -q '^DONE' "$f" 2>/dev/null && return
  if [ "$m" = plain ]; then /Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-02-rees-schedules/small-prime/dfs2b $k $p $p 1000000000000000 plain print > "$f" 2>&1
  else /Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-02-rees-schedules/small-prime/dfs2b $k $p $p 1000000000000000 print > "$f" 2>&1; fi; }
export -f one
xargs -P "$N" -L 1 bash -c 'one "$@"' _ < queue.txt
echo ALL_DONE > out/ALL_DONE
