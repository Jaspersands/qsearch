#!/bin/sh
# verify.sh : independent check of all sweep outputs (strict witnesses + coverage).
# Writes verify_hi.out.  Safe to run while the sweep is still going (an incomplete last
# line shows up as UNPARSED and its prime as missing).
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-t1-sweep-hi
cd "$D" || exit 1
nice -n 10 /opt/anaconda3/bin/python verify_hi.py 8388608 117441563 chunks.txt out/c*.out $(ls out/retry_w*.out 2>/dev/null) > verify_hi.out 2>&1
tail -25 verify_hi.out
