"""Write the DIMACS CNF that `gadget_cnf5.py p S k d L [--fix F]` solves, without solving it.

Same encoding (gadget_cnf5.solve4) and the same DIMACS text as gadget_cnf5.external_solve, so the
sha256 printed here equals the 'cnf_sha256' recorded in the *_split.out lines.
usage: dump_gadget_cnf.py p S k d L [--fix 'D1,D2,c:x,y;...'] --out FILE
prints one line: sha256=<hex> vars=<n> clauses=<m>
"""
import argparse
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FQ = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-08-rees-sde-fq-nest'))
sys.path.insert(0, FQ)
import gadget_cnf5 as G                      # noqa: E402
from gadget_sat import parse_S, parse_L      # noqa: E402


def parse_fix(s):
    fix = {}
    for item in filter(None, s.split(';')):
        lhs, rhs = item.split(':')
        *dv, ci = [int(x) for x in lhs.split(',')]
        fix[(tuple(dv), ci)] = tuple(int(x) for x in rhs.split(','))
    return fix


def dump(p, S, k, d, L, fix, out):
    rec = {}

    def capture(n, clauses, **ext):
        with open(out, 'w') as f:
            f.write(f'p cnf {n} {len(clauses)}\n')
            for cl in clauses:
                f.write(' '.join(map(str, cl)) + ' 0\n')
        rec.update(vars=n, clauses=len(clauses))
        return 'UNSAT', {}

    G.external_solve = capture               # solve4 looks the name up at call time
    G.solve4(p, S, k, d, L, fix=fix, ext={})
    with open(out, 'rb') as f:
        rec['sha256'] = hashlib.sha256(f.read()).hexdigest()
    return rec


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('k', type=int)
    ap.add_argument('d', type=int); ap.add_argument('L')
    ap.add_argument('--fix', default=''); ap.add_argument('--out', required=True)
    A = ap.parse_args()
    S = parse_S(A.p, A.S); L = parse_L(A.p, A.k, A.L)
    r = dump(A.p, S, A.k, A.d, L, parse_fix(A.fix), A.out)
    print(f"sha256={r['sha256']} vars={r['vars']} clauses={r['clauses']}", flush=True)
