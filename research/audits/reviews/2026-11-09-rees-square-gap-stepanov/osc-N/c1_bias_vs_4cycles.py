"""Compare N1/mu1 (column C1/T1*k^((k-1)^2) of ../types/sep_k{3,4}.out) with exp(-(k-1)C(k,2)^2/(p-2)),
the heuristic that the (k-1)C(k,2)^2 kernel 4-cycle frequencies, each = -1/(p-2) relative on the open
stratum to leading order, exponentiate.  Usage: python c1_bias_vs_4cycles.py"""
import math, os
here = os.path.dirname(os.path.abspath(__file__))
for k in (3, 4):
    n4 = (k - 1) * math.comb(k, 2) ** 2
    print(f'k={k}: number of kernel 4-cycle frequencies = {n4}')
    for line in open(os.path.join(here, '..', 'types', f'sep_k{k}.out')):
        f = line.split()
        if len(f) < 12 or not f[0].isdigit() or f[2] == 'no' or 'nice' in line:
            continue
        p = int(f[1]); r = float(f[11])
        pred = math.exp(-n4 / (p - 2))
        print(f'  p={p:4d}  N1/mu1={r:.3f}  exp(-n4/(p-2))={pred:.3f}  (1-1/(p-2))^n4={(1-1/(p-2))**n4:.3f}  ratio={r/pred:.3f}')
