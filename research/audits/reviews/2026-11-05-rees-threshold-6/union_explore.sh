#!/bin/sh
# For each kappa and each prime in the current tower-exceptional list, test union chains
#   Z_kappa -> K -> {0}  for every K containing 0 with |K| in {2,3} (complete search).
try() { k=$1; shift; for p in "$@"; do
  for K in $(python3 -c "
import itertools
k=$k
for s in (1,2):
  for c in itertools.combinations(range(1,k),s): print(','.join(map(str,(0,)+c)))"); do
    full=$(python3 -c "print(','.join(map(str,range($k))))")
    a=$(./rectu $k "$full" "$K" $p $p 1 | awk '{print $2}'); [ "$a" = FEASIBLE ] || continue
    b=$(./rectu $k "$K" "0" $p $p 1 | awk '{print $2}'); [ "$b" = FEASIBLE ] || continue
    echo "kappa=$k p=$p covered by K=$K"; break
  done; done; }
try 4 5 13 29
try 6 7 13 19 31 43 67 79 139
try 8 17 41 73 89 137 233 761
try 9 19 37 73 109 127 163 181 199 271 307 379 433 487 523
try 7 29 43 71 113
try 5 11
