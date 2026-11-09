#!/bin/zsh
# Negative and positive controls for lrat-check. A run counts as VERIFIED only if the checker exits 0
# and prints the line "c VERIFIED". Every control has an expected verdict for the fixed build; the
# upstream build is run for comparison only (column '-' if it is not built). Exit status 1 if the
# checker under test misses any expectation; batch runners call this as a preflight.
# usage: ./controls.sh [checker-under-test [upstream-binary]]
set -u
D=${0:A:h}
FIX=${1:-$D/lrat-check}
UP=${2:-$D/lrat-check-upstream}
C=$D/controls
verdict() {  # binary cnf proof -> VERIFIED | REJECTED | CRASH(rc)
  local out rc
  out=$(nice -n 19 $1 $2 $3 2>&1); rc=$?
  if [[ $rc -eq 0 ]] && print -r -- "$out" | grep -qx 'c VERIFIED'; then print VERIFIED
  elif print -r -- "$out" | grep -qx 'c NOT VERIFIED'; then print REJECTED
  else print "REJECTED(no verdict, rc=$rc)"; fi
}
# name | CNF (satisfiable or not) | proof | expected verdict of the fixed build
controls=(
  "sat_1 + one-line proof '2 0 0' (audit X1)|sat_1.cnf|empty_nohint.lrat|REJECTED"
  "sat_1 + '2 0 1 0' (empty clause, satisfied hint)|sat_1.cnf|empty_hint1.lrat|REJECTED"
  "sat_1 + '2 0 1 -1 0' (empty clause with a RAT hint)|sat_1.cnf|empty_rathint.lrat|REJECTED"
  "sat_1 + '2 0 99999 0' (hint to an unused index)|sat_1.cnf|empty_badid.lrat|REJECTED"
  "sat_1 + pure-literal lemma then empty clause|sat_1.cnf|pure_then_empty.lrat|REJECTED"
  "sat_1 + '1 0 0' (lemma reuses index 1)|sat_1.cnf|reuse_id.lrat|REJECTED"
  "sat_or + one-line proof '2 0 0'|sat_or.cnf|empty_nohint.lrat|REJECTED"
  "sat_2units + one-line proof '3 0 0'|sat_2units.cnf|empty_nohint_m2.lrat|REJECTED"
  "sat_2units + '3 0 1 2 0' (hints satisfied, no conflict)|sat_2units.cnf|empty_2hints.lrat|REJECTED"
  "php54_sat (SAT, same clause ids) + CaDiCaL proof of php54|php54_sat.cnf|php54.lrat|REJECTED"
  "unsat_1 + wrong hint '3 0 1 0'|unsat_1.cnf|unsat_badhint.lrat|REJECTED"
  "php54 + CaDiCaL proof without its last (empty-clause) line|php54.cnf|php54_trunc.lrat|REJECTED"
  "unsat_1 + correct proof '3 0 1 2 0'|unsat_1.cnf|unsat_good.lrat|VERIFIED"
  "php54 (pigeonhole 5 into 4, UNSAT) + CaDiCaL 3.0.1 LRAT proof|php54.cnf|php54.lrat|VERIFIED"
)
print "fixed:    ${FIX:t} (sha256 $(shasum -a 256 $FIX | cut -c1-16))"
[[ -x $UP ]] && print "upstream: ${UP:t} (sha256 $(shasum -a 256 $UP | cut -c1-16))"
print "| control | expected | checker under test | upstream build |"
print "|---|---|---|---|"
bad=0
for row in $controls; do
  IFS='|' read -r name cnf prf exp <<< "$row"
  vf=$(verdict $FIX $C/$cnf $C/$prf); vu=-; [[ -x $UP ]] && vu=$(verdict $UP $C/$cnf $C/$prf)
  [[ ${vf%%\(*} == $exp ]] || { bad=$((bad+1)); vf="$vf  <-- WRONG"; }
  print "| $name | $exp | $vf | $vu |"
done
if [[ $bad -eq 0 ]]; then print "CONTROLS OK: the checker under test matched all ${#controls} expectations"; exit 0
else print "CONTROLS FAILED: $bad of ${#controls} expectations missed"; exit 1; fi
