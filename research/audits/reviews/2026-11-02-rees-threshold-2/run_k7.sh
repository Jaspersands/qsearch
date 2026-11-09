#!/bin/zsh
# kappa = 7 complete-or-witness scan, (4621, 5e6] in 4 chunks, node limit 1e9.
cd "$(dirname $0)"
./sdfs 7 4622 1000000 1000000000 11 > k7_a.out &
./sdfs 7 1000001 2300000 1000000000 12 > k7_b.out &
./sdfs 7 2300001 3700000 1000000000 13 > k7_c.out &
./sdfs 7 3700001 5000000 1000000000 14 > k7_d.out &
wait
