#!/bin/sh
# Proposition 4.7 check: RC(10; {0,2,4,6,8}) (the last step of the tower 2 | 10) projects onto a
# two-level contraction at kappa = 5, so it must be INFEASIBLE at every p in E_2(5).
# Controls: primes p = 1 (mod 10) outside E_2(5).  Complete DFS of rectu.c (distinct beta, zeros allowed).
for p in 11 31 41 61 71 101 131 151 181; do ALLOWDUP=0 ./rectu 10 "0,2,4,6,8" "0" $p $p 1 1; done
echo "controls (p not in E_2(5)):"
for p in 191 211 241 251 271 281 311 331; do ALLOWDUP=0 ./rectu 10 "0,2,4,6,8" "0" $p $p 1 1; done
echo "controls at p ~ 1e6 (randomized mode; witnesses re-checked by check_pair below):"
ALLOWDUP=0 ./rectu 10 "0,2,4,6,8" "0" 1000000 1000200 0 1 5 300 10 | tee /dev/stderr | /opt/anaconda3/bin/python -c "
import sys; sys.path.insert(0,'.')
from adaptive_chain import check_pair
for line in sys.stdin:
    t=line.split(); p=int(t[0]); g=int(t[2].split('=')[1]); bi=t.index('beta'); ai=t.index('alpha')
    R=[0,2,4,6,8]; beta=dict(zip(R,map(int,t[bi+1:ai]))); alpha=list(map(int,t[ai+1:ai+11]))
    print(p,'witness check:',check_pair(p,g,10,R,[0],alpha,beta))"
