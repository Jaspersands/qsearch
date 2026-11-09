"""Same reduced CNF as gadget_cnf4 but solved by z3 (second engine, for cross-checking verdicts)."""
import sys, time, itertools
import z3
import gadget_cnf4 as g4
from gadget_sat import parse_S, parse_L

p, Sspec, k, d, Lspec = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
S = parse_S(p, Sspec); L = parse_L(p, k, Lspec)
# monkeypatch pycosat.solve inside gadget_cnf4 with a z3 CNF solver
class Z3Solver:
    @staticmethod
    def solve(clauses):
        n = max(abs(x) for c in clauses for x in c)
        v = [None] + [z3.Bool(f'x{i}') for i in range(1, n + 1)]
        s = z3.Solver()
        for c in clauses:
            s.add(z3.Or([v[x] if x > 0 else z3.Not(v[-x]) for x in c]))
        r = s.check()
        if r != z3.sat:
            return 'UNSAT'
        m = s.model()
        return [i if z3.is_true(m[v[i]]) else -i for i in range(1, n + 1)]
g4.pycosat = Z3Solver
t0 = time.time()
r, sol, dt = g4.solve4(p, S, k, d, L, weak=True, verbose=True)
print(f'[z3] p={p} S={S} k={k} d={d} L={Lspec}: {r.upper()} [{time.time()-t0:.1f}s]', flush=True)
