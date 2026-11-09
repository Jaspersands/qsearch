#!/bin/zsh
# Build the fixed lrat-check (lrat-check.c = upstream + lrat-check.patch) and, for the negative
# controls only, the verbatim upstream copy; then run the controls (controls.out).
# usage: ./build.sh            (from any directory)
set -eu
D=${0:A:h}
cd $D
nice -n 19 cc -O2 -o lrat-check lrat-check.c
nice -n 19 cc -O2 -o lrat-check-upstream lrat-check.upstream.c
shasum -a 256 lrat-check.upstream.c lrat-check.c lrat-check.patch
./controls.sh > controls.out
tail -1 controls.out
