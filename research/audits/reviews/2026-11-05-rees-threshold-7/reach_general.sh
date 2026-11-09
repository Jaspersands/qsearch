#!/bin/sh
# general admissible chains (towers, union chains and mixed) at the primes no chain of threshold-6 covered
P=/opt/anaconda3/bin/python
$P reach.py general 5 11
$P reach.py general 6 7 13 19 31 43 67
$P reach.py general 7 29 43 71
$P reach.py general 8 17 41 73 89 137 233
$P reach.py general 9 19 37 73 109 127 163 181 199 307 433
$P reach.py general 4 5 13   # appended after the main run
