#!/bin/zsh
# Complete dfs2b searches (existing code, 2026-11-02-rees-schedules/small-prime/dfs2b.c) for kappa = 10..16
# on small ranges. INFEASIBLE = member of E_2(kappa); LIMIT = no conclusion (node cap 3e7 per prime).
B=../2026-11-02-rees-schedules/small-prime/dfs2b
for k in 10 11 12 13 14 15 16; do
  timeout 240 nice -n 10 $B $k 3 40000 30000000 print > dfs2b_k${k}.out 2>&1
  echo "k=$k exit=$? $(grep -c INFEASIBLE dfs2b_k${k}.out) inf, $(grep -c '^FEASIBLE' dfs2b_k${k}.out) feas, $(grep -c '^LIMIT' dfs2b_k${k}.out) limit, last: $(tail -1 dfs2b_k${k}.out | cut -c1-60)"
done
