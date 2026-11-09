#!/bin/zsh
# Re-certify the (p, kappa) = (7, 2) unsplit cell with the fixed checker. Regenerates the CNF that
# `gadget_cnf5.py 7 pow:2 2 2 nest` solves (no case split; 9 Nov original: 1134 vars, 106100
# clauses, CaDiCaL 1436 s incl. a 396 s check, proof 12,293,854,888 bytes), solves it with CaDiCaL
# using gadget_cnf5's flags, and checks the LRAT proof with ../lrat-check. The proof is deleted
# after it is hashed (it is about 12 GB). usage: WORK=<scratch dir> ./unsplit_7_2.sh > unsplit_7_2.out
set -u
D=${0:A:h}; R=${D:h}
W=${WORK:?set WORK to a scratch directory}/unsplit_7_2; mkdir -p $W
PY=/opt/anaconda3/bin/python
$R/controls.sh > $W/controls_pre.out || { print "controls failed; stop"; exit 1; }
print "controls: $(tail -1 $W/controls_pre.out)"
print "cadical $(cadical --version)  checker sha256 $(shasum -a 256 $R/lrat-check | cut -c1-16)"
print "start $(date)"
nice -n 19 $PY -I $D/dump_gadget_cnf.py 7 pow:2 2 2 nest --out $W/u72.cnf
/usr/bin/time -p nice -n 19 cadical -q --lrat=true --binary=false $W/u72.cnf $W/u72.lrat 2>&1
print "cadical exit $? (20 = UNSAT)"
print "proof bytes $(stat -f %z $W/u72.lrat)"
/usr/bin/time -p nice -n 19 $R/lrat-check $W/u72.cnf $W/u72.lrat 2>&1 | grep -v '^c allocated'
print "lrat-check exit $pipestatus[1]"
print "proof sha256 $(nice -n 19 shasum -a 256 $W/u72.lrat | cut -d' ' -f1)"
rm -f $W/u72.lrat
print "end $(date)"
