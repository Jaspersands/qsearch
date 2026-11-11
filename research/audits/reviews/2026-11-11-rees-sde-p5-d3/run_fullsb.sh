#!/bin/zsh
# Re-certify the full-set cases m = 1, 2, 3 of session A with the FIXED lrat-check.
# usage: run_fullsb.sh WORKDIR   (CNFs written by full_sb.py; proofs go to WORKDIR and are deleted after)
W=$1; HERE=${0:A:h}; CHK=$HERE/../2026-11-09-lrat-checker-fix/lrat-check
for m in 1 2 3; do (
  cnf=$W/fullsb_m$m.cnf; prf=$W/fullsb_m$m.lrat; out=$HERE/fullsb_m$m.out
  { echo "cnf sha256 $(shasum -a 256 $cnf | cut -c1-64)"; echo "checker sha256 $(shasum -a 256 $CHK | cut -c1-64)"
    t0=$(date +%s); nice -n 10 cadical -q --lrat=true --binary=false $cnf $prf; echo "cadical exit $? ($(( $(date +%s)-t0 )) s)"
    echo "proof bytes $(stat -f %z $prf)"
    t0=$(date +%s); nice -n 10 $CHK $cnf $prf | grep -E '^c (VERIFIED|NOT VERIFIED)|failed'; echo "lrat-check exit ${pipestatus[1]} ($(( $(date +%s)-t0 )) s)"
    rm -f $prf; echo DONE; } > $out 2>&1 ) &
done; wait
