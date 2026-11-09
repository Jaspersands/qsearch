#!/bin/sh
# verify.sh : re-check every sweep output with two independent verifiers.
#  (1) verify_k9.py (this folder): strict and non-strict witnesses, coverage, exceptions,
#      contiguous bound X; writes verify_k9.out.
#  (2) ../2026-11-04-rees-threshold-5/verify_witnesses.py --zeros --cover 9 20001 193710244
#      (the older, separately written checker; --zeros reports non-strict witnesses
#      separately, strict ones stay strict); writes verify_witnesses_old.out.  It is run
#      a second time without --zeros (strict only) into verify_witnesses_old_strict.out.
# Safe to run while the sweep is still going: an incomplete last line shows up as
# UNPARSED (verify_k9) or is ignored, and unreached primes count as missing.
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-k9-sweep
OLDD=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-threshold-5
PY=/opt/anaconda3/bin/python
cd "$D" || exit 1
FILES="$(ls out/c*.out out/r_c*.out out/dfs2b_*.out low/*.out 2>/dev/null)"
nice -n 10 $PY verify_k9.py 20000 193710244 chunks.txt $FILES > verify_k9.out 2>&1
tail -12 verify_k9.out
nice -n 10 $PY $OLDD/verify_witnesses.py --zeros --cover 9 20001 193710244 $FILES > verify_witnesses_old.out 2>&1
cut -c1-400 verify_witnesses_old.out | tail -3
nice -n 10 $PY $OLDD/verify_witnesses.py --cover 9 20001 193710244 $FILES > verify_witnesses_old_strict.out 2>&1
cut -c1-400 verify_witnesses_old_strict.out | grep -v '^BAD' | tail -2
echo "strict-mode BAD lines (expected = number of non-strict witness lines): $(grep -c '^BAD' verify_witnesses_old_strict.out)"
