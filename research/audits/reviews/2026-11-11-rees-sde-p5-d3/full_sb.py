# Exact symmetry breaking for L = F_5^3 \ 0 (argument in the session's "Symmetry-breaking arguments";
# summarised in ../2026-11-11-rees-sde-p5-d3.md).  Copied verbatim (2026-11-11) from cloud session
# claude.ai/code/session_01B1JoCiWoB7SSi6bhNMLfEj; the only change is the CLI below: it writes the CNF
# and returns, so the solve and proof check are run separately (run_fullsb.sh).
import sys, time, pickle, subprocess
from labelsat import *
p, d = 5, 3
L = nonzero(p, d)
def build(m, step23=True):
    nv, cl, info = encode(L)
    Li = {l: i for i, l in enumerate(info['L'])}; PV = info['PHIV']
    supp = [sum(1 for x in f if x) for f in PV]; key = [(supp[k], k) for k in range(len(PV))]
    e1, e2, e3 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    cl.append([info['phi'][Li[e1]][PV.index(tuple([1] * m + [0] * (3 - m)))]])
    for l in L:
        for k in range(len(PV)):
            if supp[k] > m: cl.append([-info['phi'][Li[l]][k]])
    if step23:
        for (e, excl) in [(e2, lambda v: v[1] == 0 and v[2] == 0), (e3, lambda v: v[2] == 0)]:
            for v in L:
                if excl(v) or v == e: continue
                for k in range(len(PV)):
                    for k2 in range(len(PV)):
                        if key[k] > key[k2] and supp[k] <= m and supp[k2] <= m:
                            cl.append([-info['phi'][Li[v]][k], -info['phi'][Li[e]][k2]])
    return nv, cl, info
if __name__ == '__main__':
    m = int(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'fullsb_m%d.cnf' % m
    nv, cl, info = build(m); write_cnf(out, nv, cl); print('m', m, 'vars', nv, 'clauses', len(cl), out)
