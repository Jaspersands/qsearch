#!/bin/sh
# retry.sh LIST OUT : for each prime p in LIST (one per line), try in order, stopping at
# the first FOUND line for p (every attempt's output line is appended to OUT).
# p <= 2e7 (full index table, "tab", one byte per residue):
#  (1) famsym9 T1 tab, 20000 nodes x 5 restarts, seed 77                  [strict]
#  (2) famsym9 fam=P tab, 20000 nodes x 20 restarts, seed 79               [non-strict]
#  (3) famsym9 fam=P tab complete (all b = 1..8, budget 1e8), under a 15 s
#      wall-clock cap (timeout(1)); if cut off it prints nothing and the line
#      "TIMEOUT Pcomplete p=..." is added to OUT (no conclusion)            [non-strict]
# The exhaustive T1 search (old famsym complete) and the generic famsearch cost minutes
# per prime at p ~ 2e5-4e5 and are NOT run here; primes left over are UNRESOLVED and are
# listed as exceptions (a deferred pass can decide them).
# p > 2e7:
#  (1) famsym9 T1 ints=800000, 1e6 nodes x 20 restarts, seed 77           [strict]
#  (2) famsym9 T1 ints=1200000, 1e6 nodes x 20 restarts, seed 78          [strict]
#  (3) famsym9 fam=P win=24576, 2000 nodes x 20 restarts, seed 79         [non-strict]
# A P witness has 9 zero cells: it shows p notin E_2(9), not the strict N > 0.
# A prime with no witness after these is written as "UNRESOLVED p=...".
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-k9-sweep
OLDD=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-threshold-5
cd "$D" || exit 1
: >> "$2"
have() { grep -q "^FOUND k=9 p=$1 " "$2"; }
run() { "$@" < /dev/null | grep -v "^DONE" >> "$OUT"; }
capped() { st=$1; cap=$2; shift 2; timeout $cap "$@" < /dev/null > cap_$$.tmp; rc=$?; grep -v "^DONE" cap_$$.tmp >> "$OUT"; rm -f cap_$$.tmp
           [ $rc -eq 124 ] && echo "TIMEOUT $st p=$p" >> "$OUT"; }
OUT="$2"
while read p; do
  [ -z "$p" ] && continue
  have $p "$OUT" && continue
  grep -q "^UNRESOLVED p=$p\$" "$OUT" && continue
  if [ "$p" -le 20000000 ]; then
    run ./famsym9 9 $p $p 20000 5 77 tab;                  have $p "$OUT" && continue
    run ./famsym9 9 $p $p 20000 20 79 tab fam=P;           have $p "$OUT" && continue
    capped Pcomplete 15 ./famsym9 9 $p $p 100000000 8 1 complete tab fam=P; have $p "$OUT" && continue
  else
    run ./famsym9 9 $p $p 1000000 20 77 ints=800000;       have $p "$OUT" && continue
    run ./famsym9 9 $p $p 1000000 20 78 ints=1200000;      have $p "$OUT" && continue
    run ./famsym9 9 $p $p 2000 20 79 win=24576 fam=P
  fi
  have $p "$OUT" || echo "UNRESOLVED p=$p" >> "$OUT"
done < "$1"
