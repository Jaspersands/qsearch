#!/bin/sh
# F3 (two-progression family) at kappa = 7 on sampled primes in four bands; run with nice.
./two_prog 7 30000 32000 3      # ~10 primes near 3e4
./two_prog 7 60000 62500 4      # ~8 primes near 6e4
./two_prog 7 120000 122500 5    # ~6 primes near 1.2e5
./two_prog 7 240000 240700 4    # ~2 primes near 2.4e5
