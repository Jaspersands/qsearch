#!/bin/sh
# retry.sh LIST OUT : for each prime in LIST, try in order
#  (1) famsym_direct, wider window 12288, 1e6 nodes, 20 restarts;
#  (2) famsearch auto (H family when h even, else full), 200000 nodes, 2000 restarts;
#  (3) original famsym complete (table-based; decides whether T1 has a strict solution).
# Every attempt's output line is appended to OUT; the first FOUND stops the chain.
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-t1-sweep-hi
OLDD=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-threshold-5
cd "$D" || exit 1
: >> "$2"
while read p; do
  [ -z "$p" ] && continue
  grep -q "^FOUND k=8 p=$p " "$2" && continue
  ./famsym_direct 8 $p $p 1000000 20 77 win=12288 | grep -v '^DONE' >> "$2"
  grep -q "^FOUND k=8 p=$p " "$2" && continue
  $OLDD/famsearch 8 $p $p auto 200000 2000 77 | grep -v '^DONE' >> "$2"
  grep -q "^FOUND k=8 p=$p " "$2" && continue
  $OLDD/famsym 8 $p $p 100000000 8 1 complete | grep -v '^DONE' >> "$2"
  grep -q "^FOUND k=8 p=$p " "$2" || echo "UNRESOLVED p=$p" >> "$2"
done < "$1"
