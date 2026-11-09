#!/bin/zsh
# Re-certify the k = 3, p = 7 (kappa = 2, nested set) cell with the fixed checker, without the
# gamma_(1,1) split: each of the two first-slot cases of cases7k3.txt (the two-case cover is proved
# in referee C's report, section C) is solved as ONE CNF by CaDiCaL (gadget_cnf5's flags, wall-clock
# cap 3600 s), its LRAT proof is checked with ../lrat-check, hashed and deleted.
# Encoding tie-in, per case: the CNF of one recorded sub-case of k3_7_split.out is regenerated; its
# sha256 must equal the recorded cnf_sha256, and it must be the case CNF plus trailing unit clauses
# (so every sub-case CNF of the split is the case CNF plus units, and case UNSAT covers them all).
# usage: WORK=<scratch dir> ./k3_7_cases.sh > k3_7_cases.out 2>&1
set -u
D=${0:A:h}; R=${D:h}
W=${WORK:?set WORK to a scratch directory}/k3_7_cases; mkdir -p $W
PY=/opt/anaconda3/bin/python
$R/controls.sh > $W/controls_pre.out || { print "controls failed; stop"; exit 1; }
print "controls: $(tail -1 $W/controls_pre.out)"
print "cadical $(cadical --version)  checker sha256 $(shasum -a 256 $R/lrat-check | cut -c1-16)"
print "start $(date)"

run_case() {
  local tag=$1 fix=$2 subfix=$3 subsha=$4
  print "== $tag: case fix=$fix"
  nice -n 19 $PY -I $D/dump_gadget_cnf.py 7 pow:2 3 2 nest --fix "$fix" --out $W/$tag.cnf
  print "tie-in sub-case fix=$fix;$subfix (recorded cnf_sha256 $subsha)"
  nice -n 19 $PY -I $D/dump_gadget_cnf.py 7 pow:2 3 2 nest --fix "$fix;$subfix" --out $W/$tag.sub.cnf
  nice -n 19 $PY -I - $W/$tag.cnf $W/$tag.sub.cnf $subsha <<'EOF'
import hashlib, sys
case, sub, want = sys.argv[1], sys.argv[2], sys.argv[3]
h = hashlib.sha256(open(sub, 'rb').read()).hexdigest()
A = open(case).read().splitlines(); B = open(sub).read().splitlines()
prefix = B[1:len(A)] == A[1:]
tail = B[len(A):]
units = all(len(t.split()) == 2 and t.split()[1] == '0' for t in tail)
same_vars = A[0].split()[2] == B[0].split()[2]
ok = h == want and prefix and units and same_vars
print(f"tie-in: sha256 {'equal' if h == want else 'DIFFERENT ' + h}; case clauses are a prefix: {prefix}; "
      f"{len(tail)} extra clauses, all units: {units}; same vars: {same_vars} -> {'OK' if ok else 'FAIL'}")
EOF
  rm -f $W/$tag.sub.cnf
  /usr/bin/time -p nice -n 19 cadical -q -t 3600 --lrat=true --binary=false $W/$tag.cnf $W/$tag.lrat 2>&1
  local rc=$?
  print "cadical exit $rc (20 = UNSAT, 0 = unknown / time limit)"
  if [[ $rc == 20 ]]; then
    print "proof bytes $(stat -f %z $W/$tag.lrat)"
    /usr/bin/time -p nice -n 19 $R/lrat-check $W/$tag.cnf $W/$tag.lrat 2>&1 | grep -v '^c allocated' | grep -v '^c increasing'
    print "lrat-check exit $pipestatus[1]"
    print "proof sha256 $(nice -n 19 shasum -a 256 $W/$tag.lrat | cut -d' ' -f1)"
  fi
  rm -f $W/$tag.lrat
  print "end $tag $(date)"
}

run_case case1 "1,0,1:3,0,0" "1,1,0:2,5,1" b3edc61c791111bb08fc4dc87874a9b1276fccc2dd474641cbb44549999176f1 > $W/case1.log 2>&1 &
run_case case2 "1,0,1:0,3,0" "1,1,0:4,0,6" 9fa82645bb95745e593425e447f2c446caa85ce37bca7633b5112594c0ec1da0 > $W/case2.log 2>&1 &
wait
cat $W/case1.log $W/case2.log
print "end $(date)"
